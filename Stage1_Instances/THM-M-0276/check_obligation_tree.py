#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for the THM-M-0276 obligation freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0276-OBLIGATION_TREE"
THEOREM = "THM-M-0276"
ROOT_ID = "M0276-ROOT"
BASE_REVISION = "b243ebc0f9058ba5afafef8240b92c2dfb2edc6e"
BASE_TREE = "b4b092069141ac54ea1ab5a6ea946192a30ec78c"
STATEMENT_SHA256 = "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea"
ANCHOR_SHA256 = "d84027b9f12d99c5617d719f7ce48bb1b34917a90414f476589e53c17934b906"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BANACH_BLOB = "8d4361a5bdf07bb8b7e2214ee59340f9931422bd"
BANACH_SHA256 = "b046e38a239014c32e2313b4a216edd89198e57351d9c6068a3de7811680bf6c"
GRAPH_NAMES = {
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
}
REGISTRY_FIELDS = {
    "obligation_id",
    "statement_fingerprint",
    "kind",
    "root_relevant",
    "machine_eligibility",
    "human_source_eligibility",
    "readable_eligibility",
    "risk_class",
    "exclusion_reason",
    "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id",
    "obligation_id",
    "kind",
    "human_statement",
    "formal_target",
    "output",
    "human_debt",
    "machine_debt",
    "readability_debt",
    "evidence_ids",
    "source_crosswalk_id",
    "provenance_id",
    "foundation_profile",
    "tcb_profile",
    "computation_record",
    "step_budget",
    "semantic_step_ledger",
    "public_readable_target",
    "validation_spec_id",
    "status_boundary",
    "task_ids",
    "owned_sources",
    "owner",
    "reviewer",
    "validity",
}
ALLOWED_EDGES = {
    "proof_requires",
    "composes",
    "logical_decomposition",
    "expository_decomposition",
    "equivalent_to",
    "transports",
    "source_map",
    "provenance_of",
    "evidence_for",
    "trusts",
    "documents",
    "workflow_depends_on",
}
PACKET_FILES = {
    "ObligationTree.lean",
    "build_obligation_artifacts.py",
    "check_obligation_tree.py",
    "obligation-registry.json",
    "typed-graphs.json",
    "validation-specs.json",
    "obligation-tree.md",
    "obligation-tree-validation.md",
    "obligation-tree-receipt.json",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


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


def run_lean() -> str:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    run = subprocess.run(
        [
            "lake",
            "env",
            "lean",
            "--trust=0",
            "../../Stage1_Instances/THM-M-0276/ObligationTree.lean",
        ],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        raise SystemExit(run.returncode)
    return run.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    local_dag = load("task-dag.json")
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )

    expected_registry, expected_bundle, expected_specs, expected_markdown = (
        build_obligation_artifacts.build()
    )
    expected_outputs = {
        "obligation-registry.json": canonical_json(expected_registry),
        "typed-graphs.json": canonical_json(expected_bundle),
        "validation-specs.json": canonical_json(expected_specs),
        "obligation-tree.md": expected_markdown.encode(),
    }
    for name, expected in expected_outputs.items():
        assert (HERE / name).read_bytes() == expected, f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert (
        registry["theorem_id"]
        == bundle["theorem_id"]
        == specs["theorem_id"]
        == THEOREM
    )
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0276-OBLIGATIONS-v1"
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1282
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1282
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0276-ANCHOR_AUDIT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == item["depends_on"][0])
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_dag["accepted_states"] == []

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 29
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    for row in rows:
        assert row["root_relevant"] is True
        assert row["kind"] in {
            "root",
            "definition",
            "normalization",
            "reduction",
            "branch",
            "construction",
            "bridge",
            "core_lemma",
            "computation",
            "certificate",
            "transport",
            "terminal",
        }
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        excluded = not (
            row["machine_eligibility"]
            == row["human_source_eligibility"]
            == row["readable_eligibility"]
            == "required"
        )
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert row["exclusion_reason"]["approval"].startswith("pending independent")

    fields = tuple(registry["canonical_projection_fields"])
    assert set(fields) == REGISTRY_FIELDS
    denominator = canonical_digest([{key: row[key] for key in fields} for row in rows])
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[eligibility] == "required"
        ]
    assert registry["status_observed_after_freeze"]["closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["accepted_root_machine_debt"] == "M3"
    assert registry["status_observed_after_freeze"]["candidate_closure_credit"] is False
    assert "M1/E2" in registry["status_observed_after_freeze"]["candidate_route"]
    assert (
        next(row for row in rows if row["obligation_id"] == "M0276-B-REAL")[
            "terminal_proof_body_id"
        ]
        == next(row for row in rows if row["obligation_id"] == "M0276-B-COMPLEX")[
            "terminal_proof_body_id"
        ]
    )

    nodes = bundle["nodes"]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0276-")
        assert node["human_debt"] == "H2"
        assert node["machine_debt"] in {"M3", "M5"}
        assert node["readability_debt"] == "R4"
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {
                "step_id",
                "premise_ids",
                "inference",
                "source_locator",
                "output",
                "outgoing_use",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validation_spec_id"] == "VAL-M0276-OBLIGATION-BUNDLE"
        assert node["task_ids"] == [ITEM]
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert all(not source.startswith("Formalizations/Lean/.lake") for source in node["owned_sources"])
        assert "no m0" in node["status_boundary"].lower()
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | step_ids | {"frozen-formal-context"}

    assert bundle["root_node_id"] == ROOT_ID
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0276-ANCHOR_AUDIT",
        ITEM,
        "S56-M-0276-PROOF",
        "S56-M-0276-VALIDATION",
        "S56-M-0276-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_nodes if name == "workflow" else id_set
        assert set(graph["out"]) == endpoints == set(graph["in"])
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["from"] in endpoints and edge["to"] in endpoints
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            if name == "workflow":
                assert edge["type"] == "workflow_depends_on"
            else:
                assert edge["type"] != "workflow_depends_on"
            edge_ids.add(edge["edge_id"])
            if edge["type"] not in {"composes", "logical_decomposition"} or name != "proof":
                directional.append(edge)
        if name != "proof":
            check_acyclic(directional)

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for edge in proof.values():
        reverse = proof[edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
        assert "proof_requires" in {edge["type"], reverse["type"]}
        other = reverse["type"] if edge["type"] == "proof_requires" else edge["type"]
        parent = edge["from"] if edge["type"] == "proof_requires" else reverse["from"]
        assert other == ("composes" if parent == ROOT_ID else "logical_decomposition")
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    check_acyclic(
        [edge for edge in proof.values() if edge["type"] == "proof_requires"]
    )
    reachable: set[str] = set()

    def reach(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            reach(child)

    reach(ROOT_ID)
    assert len(reachable) == 20 and set(children) <= reachable
    assert all(node_by_id[identifier]["machine_debt"] == "M3" for identifier in reachable)

    certificates = bundle["composition_certificates"]
    assert len(certificates) == 1
    certificate = certificates[0]
    assert certificate["parent_obligation_id"] == ROOT_ID
    assert certificate["required_child_ids"] == children[ROOT_ID] == [
        "M0276-T-ADAPTER",
        "M0276-T-UPSTREAM",
    ]
    assert set(certificate["checked_declarations"]) == {
        "Stage1Instances.THM_M_0276_Obligations.terminal_adapter",
        "Stage1Instances.THM_M_0276_Obligations.pinned_mathlib_terminal",
        "Stage1Instances.THM_M_0276_Obligations.compose_root",
    }
    assert certificate["introduces_undeclared_premises"] is False
    assert certificate["accepted"] is False
    assert "planned signatures" in certificate["fingerprint_binding_boundary"]
    plans = {
        row["parent_obligation_id"]: row
        for row in bundle["unverified_decomposition_plans"]
    }
    assert set(plans) == set(children) - {ROOT_ID}
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert plan["status"] == (
            "source_body_decomposition_unverified_as_child_to_parent_composition"
        )

    closure = bundle["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert "M0276-C01/E2/M1" in closure["candidate_evidence"]
    assert set(closure["remaining_machine_root_cut_set"]) == {
        "M0276-B-REAL",
        "M0276-B-COMPLEX",
    }

    assert len(specs["recipes"]) == 1
    recipe = specs["recipes"][0]
    assert recipe["recipe_id"] == "VAL-M0276-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "." and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["timeout_seconds"] == 240
    assert recipe["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0276/check_obligation_tree.py",
    ]
    assert set(recipe["covered_obligation_ids"]) == id_set
    assert "kernel coverage is limited" in recipe["coverage_boundary"]

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    banach = MATHLIB / "Mathlib/Analysis/Normed/Operator/Banach.lean"
    assert output("git", "rev-parse", "HEAD:Mathlib/Analysis/Normed/Operator/Banach.lean", cwd=MATHLIB) == BANACH_BLOB
    assert sha256(banach) == BANACH_SHA256
    source = banach.read_text(encoding="utf-8")
    for marker in (
        "theorem exists_approx_preimage_norm_le (surj : Surjective f)",
        "⋃ n : ℕ, closure (f '' ball 0 n) = Set.univ",
        "nonempty_interior_of_iUnion_of_closed",
        "rcases rescale_to_shell",
        "theorem exists_preimage_norm_le (surj : Surjective f)",
        "let h y := y - f (g y)",
        "have hnle : ∀ n : ℕ",
        "have sNu : Summable fun n => ‖u n‖",
        "have fsumeq : ∀ n : ℕ",
        "have feq : f x = y - 0 := tendsto_nhds_unique L₁ L₂",
        "protected theorem isOpenMap (surj : Surjective f) : IsOpenMap f",
        "rcases exists_preimage_norm_le f surj",
    ):
        assert marker in source, marker

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", lean_source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern|native_decide)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "def ExactRoot : Prop",
        "def MathlibTerminal : Prop",
        "theorem terminal_adapter",
        "theorem pinned_mathlib_terminal",
        "theorem compose_root",
        "theorem exactRoot_iff_canonicalStatementCopy",
        "adapter terminal",
        "exact ContinuousLinearMap.isOpenMap f hf",
        "assert_no_sorry terminal_adapter",
        "#print axioms compose_root",
    ):
        assert marker in lean_source, marker

    lean_stdout = run_lean()
    normalized = re.sub(r"\s+", " ", lean_stdout)
    assert lean_stdout.count("Declarations are sorry-free!") == 7
    assert normalized.count("propext, Classical.choice, Quot.sound") == 7
    assert "sorryAx" not in lean_stdout
    for declaration in (
        "terminal_adapter",
        "pinned_mathlib_terminal",
        "compose_root",
        "exactRoot_iff_canonicalStatementCopy",
        "ContinuousLinearMap.exists_approx_preimage_norm_le",
        "ContinuousLinearMap.exists_preimage_norm_le",
        "ContinuousLinearMap.isOpenMap",
    ):
        assert declaration in lean_stdout
    assert "And RealOpenMappingTarget.{u, v} ComplexOpenMappingTarget.{u, v}" in lean_stdout
    assert "def Stage1Instances.THM_M_0276_Obligations.CanonicalStatementCopy" in lean_stdout
    expanded_copy = re.search(
        r"def Stage1Instances\.THM_M_0276_Obligations\.CanonicalStatementCopy\.\{u, v\} : Prop :=\n"
        r"(?P<expression>.*)\Z",
        lean_stdout,
        re.DOTALL,
    )
    assert expanded_copy is not None
    assert hashlib.sha256(expanded_copy.group("expression").strip().encode()).hexdigest() == (
        "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
    )

    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["obligation_registry_hash"] == "sha256:" + denominator
    assert set(instance["owned_artifacts"]) == {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM}/{name}" for name in instance["owned_artifacts"]
    }

    receipt = load("obligation-tree-receipt.json")
    assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["closed_obligations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["obligation_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["substantive_ledger_step_count"] == len(step_ids)
    assert receipt["unverified_internal_decomposition_count"] == len(plans)
    assert receipt["lean_output_sha256"] == hashlib.sha256(lean_stdout.encode()).hexdigest()
    assert receipt["support_state"] == "worker_self_tested_pending_master_acceptance"

    status = output(
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        str(HERE),
        str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == set(receipt["changed_paths"])
    assert PACKET_FILES <= {path.name for path in HERE.iterdir() if path.is_file()}

    packet_path = args.worker_packet or ROOT / ".stage1-worker-selftest.json"
    if packet_path.is_file():
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["commands"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    for path in [*HERE.iterdir(), ROOT / ".stage1-worker-selftest.json"]:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "obligation-tree.md",
        "obligation-tree-validation.md",
        "obligation-tree-receipt.json",
        "obligation-registry.json",
        "typed-graphs.json",
        "validation-specs.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} obligations, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(
        "Lean: exact upstream terminal, specialization adapter, and root composition elaborated; "
        "seven sorry-free reports; axioms propext, Classical.choice, Quot.sound"
    )
    print("accepted root remains H2/M3/R4; closed obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
