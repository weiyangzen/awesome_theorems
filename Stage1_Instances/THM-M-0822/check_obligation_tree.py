#!/usr/bin/env python3
"""Validate the THM-M-0822 frozen registry and typed graph bundle."""

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
THEOREM = "THM-M-0822"
ITEM = "S56-M-0822-OBLIGATION_TREE"
RANK = 1380
BASE_REVISION = "f023dbc3411d83201065d1a1156d7406b81135d4"
BASE_TREE = "3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4"
ROOT_EXPRESSION = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
STATEMENT_SHA256 = "b91d0fce7cd10a12585860b11af519cbe7496f555d04a751d5b4b6309309582d"
ANCHOR_AUDIT_SHA256 = "380c1d6f3e10084bc82f24fca8a881a12fdc4794885b2e3f1ff7b5fd7985afee"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_BLOB = "f388fc0bfd201e1d9eb1279b5bd1c6dcbd253b34"
MATHLIB_SHA256 = "c6351d7ee422db9eed8f45335f4128eb3a66fe09997d12abc15eba38e9863f1c"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition",
    "expository_decomposition", "equivalent_to", "transports", "source_map",
    "provenance_of", "evidence_for", "trusts", "documents",
    "workflow_depends_on",
}
REQUIRED_NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
REQUIRED_OBLIGATION_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def check_acyclic(edges: list[dict], graph_name: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for row in edges:
        adjacency.setdefault(row["from"], []).append(row["to"])
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        assert node not in active, f"cycle in {graph_name} at {node}"
        if node in done:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        done.add(node)

    for node in adjacency:
        visit(node)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def run_lean() -> str:
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0822-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "-o", str(Path(temp_dir) / "Statement.olean"), "Statement.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        lean = subprocess.run(
            [lean_exe, "ObligationTree.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": temp_dir + ":" + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if lean.returncode:
            sys.stdout.write(lean.stdout)
            raise SystemExit(lean.returncode)
    return lean.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    instance = load("instance.json")
    task_dag = load("task-dag.json")

    expected = build_obligation_artifacts.build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"),
        expected,
    ):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated file: {name}"

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(ROOT / "Docs/Stage1_Blueprint_rev-5.6.md") == (
        "793b71efae3461278f32f200be77c2f19b88b41022360bdfa4900e1d127b0bc0"
    )
    assert sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json") == (
        "8a3404e40f1e317f35d4d25cd8f69e89f0c9515e78fab480e25a7db7ae5062ee"
    )
    assert sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json") == (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    )
    assert sha256(ROOT / "skills/execute-stage1-rev56/SKILL.md") == (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    )
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_AUDIT_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_AUDIT_SHA256

    manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == RANK
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text()
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0822-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0822"]
    assert item["deliverable"] == (
        "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    )
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0822-ANCHOR_AUDIT"
    )
    assert predecessor["state"] == "[_]"
    local_item = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and task_dag["accepted_states"] == []

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 27
    assert registry["root_obligation_id"] == bundle["root_node_id"] == "M0822-ROOT"
    allowed_kinds = {
        "root", "definition", "normalization", "reduction", "branch", "construction",
        "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
    }
    for row in rows:
        assert set(row) == REQUIRED_OBLIGATION_FIELDS
        assert row["kind"] in allowed_kinds
        assert row["root_relevant"] is True
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        assert bool(row["exclusion_reason"]) == excluded

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in rows]
    denominator = canonical_digest(projection)
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
        ("informational_overlays", "machine_eligibility", "informational"),
    ):
        assert registry["frozen_denominators"][key] == [
            row["obligation_id"] for row in rows if row[field] == value
        ]
    assert all(
        value["status"].endswith("pending_independent_approval") and value["reason"]
        for value in registry["layer_exclusions"].values()
    )
    assert registry["append_only_delta"] == []
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["accepted_root_machine_debt"] == "M3"
    metrics = registry["classification_metrics"]
    assert metrics["inventory_classified_numerator_ids"] == ids
    assert metrics["inventory_classified_denominator_ids"] == ids
    assert metrics["required_machine_leaf_denominator_ids"] == [
        "M0822-L-GROUND-ELEMENT", "M0822-L-STAR-IMAGE",
        "M0822-L-STAR-INTERSECTING", "M0822-L-STAR-SIZED",
        "M0822-T-MATHLIB-EKR",
    ]
    assert metrics["accepted_machine_leaf_numerator_ids"] == []
    assert metrics["accepted_terminal_body_numerator_ids"] == []
    assert metrics["accepted_interface_numerator_ids"] == []
    assert metrics["accepted_r0_numerator_ids"] == []
    assert metrics["accepted_h0_numerator_ids"] == []
    assert metrics["root_closed"] is metrics["critical_path_closed"] is False
    assert metrics["required_readable_denominator_ids"] == ids
    assert set(metrics["required_human_source_denominator_ids"]) == {
        row["obligation_id"] for row in rows
        if row["human_source_eligibility"] == "required"
    }
    source_boundary = {
        row["obligation_id"] for row in rows
        if row["machine_eligibility"] in {"required", "informational"}
    }
    assert set(metrics["required_formal_source_boundary_denominator_ids"]) == source_boundary
    assert set(metrics["classified_formal_source_boundary_numerator_ids"]) == source_boundary
    assert set(metrics["risk_bucket_accepted_ids"]) == {
        "critical", "high", "normal", "low",
    }
    assert all(not values for values in metrics["risk_bucket_accepted_ids"].values())
    assert metrics["disputed_eligibility_bounds"]["optimistic_accepted_machine_ids"] == []
    assert metrics["disputed_eligibility_bounds"]["pessimistic_accepted_machine_ids"] == []

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) == len({node["node_id"] for node in nodes})
    assert {node["obligation_id"] for node in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    allowed_external = {"frozen-formal-context", "pinned-mathlib-source"}
    for node in nodes:
        assert set(node) == REQUIRED_NODE_FIELDS
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M3", "M4"}
        assert node["readability_debt"] == "R4"
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator", "output",
                "outgoing_use",
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert set(step["premise_ids"]) <= id_set | allowed_external
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0822/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validation_spec_id"] == "VAL-M0822-OBLIGATION-BUNDLE"
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert "no m0" in node["status_boundary"].lower()
        assert node["task_ids"] and node["task_ids"][0] == ITEM

    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    edge_ids: set[str] = set()
    for graph_name, graph_value in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        endpoints = workflow_nodes if graph_name == "workflow" else id_set
        for row in graph_value["edges"]:
            assert row["edge_id"] not in edge_ids
            assert row["type"] in ALLOWED_EDGES
            assert row["from"] in endpoints and row["to"] in endpoints
            if graph_name == "workflow":
                assert row["type"] == "workflow_depends_on"
            else:
                assert row["type"] != "workflow_depends_on"
            expected_out.setdefault(row["from"], []).append(row["edge_id"])
            expected_in.setdefault(row["to"], []).append(row["edge_id"])
            edge_ids.add(row["edge_id"])
        assert graph_value["out"] == expected_out
        assert graph_value["in"] == expected_in
        if graph_name != "proof":
            check_acyclic(graph_value["edges"], graph_name)
    assert len(edge_ids) == 49

    proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for row in proof.values():
        assert row["type"] in {"proof_requires", "composes"}
        reverse = proof[row["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == row["edge_id"]
        assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
        assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
        if row["type"] == "proof_requires":
            children.setdefault(row["from"], []).append(row["to"])
    expected_reachable = {
        "M0822-ROOT", "M0822-T-ASSEMBLE", "M0822-T-ATTAINMENT",
        "M0822-C-STAR", "M0822-L-STAR-IMAGE", "M0822-L-STAR-INTERSECTING",
        "M0822-L-STAR-SIZED", "M0822-L-STAR-CARD", "M0822-L-GROUND-ELEMENT",
        "M0822-T-UPPER-ADAPTER", "M0822-T-MATHLIB-EKR",
    }
    reachable: set[str] = set()

    def visit(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            visit(child)

    visit("M0822-ROOT")
    assert reachable == expected_reachable

    certificates = {
        row["parent_obligation_id"]: row for row in bundle["composition_certificates"]
    }
    assert set(certificates) == set(children)
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {
            child: fingerprints[child] for child in children[parent]
        }
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
    assert {
        parent: certificate["declaration"]
        for parent, certificate in certificates.items()
    } == {
        "M0822-ROOT": (
            "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly"
        ),
        "M0822-T-ASSEMBLE": (
            "Stage1Instances.THM_M_0822.ObligationTree.composeRoot"
        ),
        "M0822-T-ATTAINMENT": (
            "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages"
        ),
        "M0822-C-STAR": (
            "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement"
        ),
        "M0822-L-STAR-CARD": (
            "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image"
        ),
        "M0822-T-UPPER-ADAPTER": (
            "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal"
        ),
    }
    assert bundle["unverified_decomposition_plans"] == []
    internal = {
        "M0822-B-RZERO", "M0822-C-COMPLEMENTS", "M0822-L-SHADOW-DISJOINT",
        "M0822-L-COMPLEMENT-CARD", "M0822-L-COMPLEMENT-SIZED",
        "M0822-L-KK-LOVASZ", "M0822-L-BINOMIAL-CONTRADICTION",
        "M0822-L-SLICE-CARD",
    }
    refinement = bundle["graphs"]["refinement"]["edges"]
    assert {
        row["to"] for row in refinement
        if row["from"] == "M0822-T-MATHLIB-EKR"
    } == internal
    assert all(
        row["type"] == "expository_decomposition"
        for row in refinement if row["to"] in internal
    )
    for identifier in internal:
        row = next(value for value in rows if value["obligation_id"] == identifier)
        assert row["machine_eligibility"] == "informational"

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == instance["accepted_proof_state"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] == "sha256:" + denominator

    assert len(specs["recipes"]) == 1
    recipe = specs["recipes"][0]
    assert set(recipe) == {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    assert recipe["recipe_id"] == "VAL-M0822-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0822/check_obligation_tree.py"
    ]
    assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and set(recipe["covered_obligation_ids"]) == id_set

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    mathlib_source = MATHLIB / "Mathlib/Combinatorics/SetFamily/KruskalKatona.lean"
    assert sha256(mathlib_source) == MATHLIB_SHA256
    assert output(
        "git", "rev-parse", "HEAD:Mathlib/Combinatorics/SetFamily/KruskalKatona.lean",
        cwd=MATHLIB,
    ) == MATHLIB_BLOB
    mathlib_text = mathlib_source.read_text(encoding="utf-8")
    for marker in (
        "theorem erdos_ko_rado", "rcases Nat.eq_zero_or_pos r",
        "have : Disjoint", "card_compls", "h₂.compls",
        "kruskal_katona_lovasz_form", "Nat.choose_succ_succ", "Set.Sized.card_le",
    ):
        assert marker in mathlib_text, marker

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|"
        r"extern|native_decide|TODO|FIXME)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "import Statement", "def AttainmentPackage : Prop",
        "def UpperBoundPackage : Prop", "def MathlibUpperBoundTerminal : Prop",
        "def GroundElementPackage : Prop", "def StarConstructionPackage : Prop",
        "def StarIntersectingPackage : Prop", "def StarSizedPackage : Prop",
        "def StarImagePackage : Prop", "def StarCardPackage : Prop",
        "theorem starConstruction_of_groundElement", "theorem starCard_of_image",
        "theorem attainment_of_starPackages",
        "theorem attainment_of_localStar", "theorem upperBound_of_mathlibTerminal",
        "theorem pinnedMathlibUpperBound", "theorem composeRoot",
        "abbrev ExactAssembly : Prop", "theorem rootOfExactAssembly",
        "#print axioms composeRoot", "#print axioms rootOfExactAssembly",
    ):
        assert marker in source, marker

    lean_stdout = run_lean()
    normalized = re.sub(r"\s+", " ", lean_stdout)
    expected_axioms = "[propext, Classical.choice, Quot.sound]"
    assert normalized.count(expected_axioms) == 8
    assert "sorryAx" not in lean_stdout and "declaration uses 'sorry'" not in lean_stdout
    for declaration in (
        "erdosKoRadoStar_attains", "Finset.erdos_ko_rado",
        "starConstruction_of_groundElement", "starCard_of_image",
        "attainment_of_starPackages",
        "attainment_of_localStar", "upperBound_of_mathlibTerminal",
        "pinnedMathlibUpperBound", "composeRoot", "rootOfExactAssembly",
    ):
        assert declaration in lean_stdout

    receipt = load("obligation-tree-receipt.json")
    assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["substantive_ledger_step_count"] == len(step_ids)
    assert receipt["composition_certificate_count"] == len(certificates)
    assert receipt["unverified_decomposition_count"] == len(
        bundle["unverified_decomposition_plans"]
    )
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["composition_declarations"] == [
        certificates[parent]["declaration"] for parent in (
            "M0822-C-STAR", "M0822-L-STAR-CARD", "M0822-T-ATTAINMENT",
            "M0822-T-UPPER-ADAPTER", "M0822-T-ASSEMBLE", "M0822-ROOT",
        )
    ]
    assert receipt["checked_candidate_declarations"] == [
        "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_localStar",
        "Stage1Instances.THM_M_0822.ObligationTree.pinnedMathlibUpperBound",
    ]
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["lean_output_sha256"] == hashlib.sha256(lean_stdout.encode()).hexdigest()
    for name, expected_hash in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected_hash, name

    if args.worker_packet:
        packet = json.loads(args.worker_packet.read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["commands"] and packet["output_summary"].startswith("PASS:")
        check_text_file(args.worker_packet)

    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)

    print(
        f"PASS THM-M-0822 obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(
        "Lean: eight conditional/candidate declarations elaborate at the exact target; "
        "no placeholders; imported body remains proof-phase candidate"
    )
    print("accepted root remains H1/M3/R4; accepted obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
