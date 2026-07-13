#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0914 obligation freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0914-OBLIGATION_TREE"
THEOREM = "THM-M-0914"
ROOT_ID = "M0914-ROOT"
EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
}
REGISTRY_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
GRAPH_EDGE_TYPES = {
    "proof": {"proof_requires", "composes"},
    "refinement": {"logical_decomposition", "expository_decomposition", "equivalent_to", "transports"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
EXPECTED_PROOF_REACHABLE = {
    "M0914-ROOT", "M0914-T-ROOT-COMPOSE", "M0914-N-FIN-CARD-INEQUALITY",
    "M0914-N-FIN-CARD-IDENTITY", "M0914-N-SUCCESSOR-LT",
    "M0914-A-FINTYPE-WRAPPER", "M0914-N-UNIV-MAPS-TO",
    "M0914-L-FINSET-COLLISION", "M0914-L-CARD-INJON-BOUND",
    "M0914-L-NO-COLLISION-INJON",
}
MACHINE_DEBTS = {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
HUMAN_DEBTS = {"H0", "H1", "H2", "H3", "H4", "H5"}
READABILITY_DEBTS = {"R0", "R1", "R2", "R3", "R4"}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def check_acyclic(edges: list[dict]) -> None:
    adjacency: dict[str, list[str]] = {}
    for edge in edges:
        adjacency.setdefault(edge["from"], []).append(edge["to"])
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        assert node not in active, f"cycle at {node}"
        if node in done:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        done.add(node)

    for node in adjacency:
        visit(node)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "LANG": "C", "TZ": "UTC", "NO_COLOR": "1"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=240,
        check=False,
    )


def composed_lean() -> subprocess.CompletedProcess[str]:
    statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
    obligation = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    body = "\n".join(
        line for line in obligation.splitlines() if not line.startswith("import ")
    ) + "\n"
    identity_marker = "\nend Stage1Instances.THM_M_0914_ObligationTree\n"
    assert body.count(identity_marker) == 1
    identity = (
        "\n/-- Validator-only identity with the actual canonical statement. -/\n"
        "theorem root_eq_actualCanonical :\n"
        "    Root = Stage1Instances.THM_M_0914.PigeonholeTarget := rfl\n"
        "assert_no_sorry root_eq_actualCanonical\n"
        "#print sorries root_eq_actualCanonical\n"
        "#print axioms root_eq_actualCanonical\n"
    )
    body = body.replace(identity_marker, identity + identity_marker)
    imports = (
        "import Mathlib.Data.Fintype.Pigeonhole\n"
        "import Mathlib.Util.AssertNoSorry\n"
        "import Mathlib.Util.PrintSorries\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(imports + statement + body)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")
    instance = load("instance.json")
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["execution_rank"] == 1456 and item["phase"] == "obligation_tree"
    assert item["layer"] == 3 and item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0914-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    expression = statement["canonical_formal_target"]["elaborated_expression_sha256"]
    assert expression == EXPRESSION_SHA256
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert anchor["canonical_target"] == "Stage1Instances.THM_M_0914.PigeonholeTarget"
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    assert instance["obligation_registry_hash"] == f"sha256:{registry['denominator_sha256']}"
    assert instance["obligation_registry_id"] == registry["registry_id"]
    assert instance["obligation_registry_version"] == registry["registry_version"]
    phase_files = {
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "obligation-tree-receipt.json",
        "obligation-tree-validation.md", "obligation-tree.md", "typed-graphs.json",
        "validation-specs.json",
    }
    assert phase_files <= set(instance["owned_artifacts"])
    assert {
        f"Stage1_Instances/{THEOREM}/{name}" for name in phase_files
    } <= set(instance["public_merge_targets"])

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids)) == 19
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    projection = [
        {field: row[field] for field in (
            "obligation_id", "statement_fingerprint", "kind", "root_relevant",
            "machine_eligibility", "human_source_eligibility", "readable_eligibility",
            "risk_class", "exclusion_reason", "terminal_proof_body_id",
        )} for row in rows
    ]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for row in rows:
        if row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required":
            assert row["exclusion_reason"], row["obligation_id"]
    assert registry["append_only_delta"] == []
    assert set(registry["layer_exclusions"]) == {
        "additional_case_splits", "construction", "computation", "transport_back"
    }
    assert all(
        "pending_independent_approval" in value["status"]
        for value in registry["layer_exclusions"].values()
    )

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
    for node in nodes:
        assert set(node) == NODE_FIELDS, node["obligation_id"]
        assert node["human_debt"] in HUMAN_DEBTS
        assert node["machine_debt"] in MACHINE_DEBTS
        assert node["readability_debt"] in READABILITY_DEBTS
        assert 0 < node["step_budget"] <= 100
        assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
        assert all(node["semantic_step_ledger"].values())
        assert node["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        readable_path, anchor_id = node["public_readable_target"].split("#", 1)
        assert readable_path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert (HERE / "obligation-tree.md").read_text(encoding="utf-8").count(
            f'<a id="{anchor_id}"></a>'
        ) == 1
        assert node["validation_spec_id"] == f"VAL-{node['obligation_id']}"
        assert ITEM in node["task_ids"] and "S56-M-0914-PROOF" in node["task_ids"]

    assert set(bundle["graphs"]) == GRAPH_NAMES
    all_edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        assert set(graph["out"]) == set(ids) and set(graph["in"]) == set(ids)
        directed_edges = graph["edges"]
        if name == "proof":
            directed_edges = [edge for edge in directed_edges if edge["type"] == "proof_requires"]
        check_acyclic(directed_edges)
        for edge in graph["edges"]:
            assert edge["edge_id"] not in all_edge_ids
            assert edge["type"] in ALLOWED_EDGES
            assert edge["type"] in GRAPH_EDGE_TYPES[name]
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            all_edge_ids.add(edge["edge_id"])
    assert len(all_edge_ids) == 45

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for edge in proof.values():
        reverse = proof[edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
        assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()

    def visit(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            visit(child)

    visit(ROOT_ID)
    assert reachable == EXPECTED_PROOF_REACHABLE

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert "aggregate fail-closed checker" in specs["recipe_scope_boundary"]
    assert {recipe["recipe_id"] for recipe in recipes} == {f"VAL-{identifier}" for identifier in ids}
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert len(recipe["covered_obligation_ids"]) == 1
        assert "Provisional aggregate architecture self-test only" in recipe["evidence_boundary"]

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    pigeonhole_source = (MATHLIB / "Mathlib/Data/Fintype/Pigeonhole.lean").read_text(encoding="utf-8")
    card_source = (MATHLIB / "Mathlib/Data/Finset/Card.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem exists_ne_map_eq_of_card_lt (f : α → β)",
        "Finset.exists_ne_map_eq_of_card_lt_of_maps_to h",
    ):
        assert marker in pigeonhole_source
    for marker in (
        "lemma card_le_card_of_injOn",
        "theorem exists_ne_map_eq_of_card_lt_of_maps_to",
        "refine hc.not_ge (card_le_card_of_injOn f hf",
    ):
        assert marker in card_source

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    lean_code = without_comments(lean_source)
    lean_code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', lean_code)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern|native_decide)\b"
    )
    assert not forbidden.search(lean_code)
    lean = composed_lean()
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    assert lean.stdout.count("Declarations are sorry-free!") == 13
    assert "root_eq_actualCanonical' does not depend on any axioms" in lean.stdout
    assert "OBLIGATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in lean.stdout
    assert "OBLIGATION_CLOSURE bodyless_nonaxioms=[]" in lean.stdout
    assert "OBLIGATION_CLOSURE unsafe=[]" in lean.stdout
    assert "sorryAx" not in lean.stdout

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    receipt = load("obligation-tree-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == 19 and receipt["typed_edge_count"] == 45
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["lean_output_sha256"] == hashlib.sha256(lean.stdout.encode()).hexdigest()
    assert receipt["artifact_hashes"] == {
        name: f"sha256:{sha256(HERE / name)}" for name in receipt["artifact_hashes"]
    }

    if args.worker_packet:
        packet_path = args.worker_packet if args.worker_packet.is_absolute() else ROOT / args.worker_packet
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"]
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["commands_and_results"]
        assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    actual_tracked = set(
        filter(None, output("git", "diff", "--name-only", "--", f"Stage1_Instances/{THEOREM}").splitlines())
    )
    actual_untracked = set(
        filter(
            None,
            output(
                "git", "ls-files", "--others", "--exclude-standard", "--",
                f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            ).splitlines(),
        )
    )
    assert actual_tracked | actual_untracked == set(receipt["changed_paths"])
    for name in receipt["changed_paths"]:
        check_text_file(ROOT / name)
    print(f"PASS {THEOREM} obligation tree: {len(ids)} obligations, {len(all_edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open; exact pinned collision route remains candidate pending downstream gates")


if __name__ == "__main__":
    main()
