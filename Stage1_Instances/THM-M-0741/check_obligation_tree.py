#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for THM-M-0741 obligations."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0741-OBLIGATION_TREE"
THEOREM = "THM-M-0741"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
STATEMENT_SHA256 = "79e8f14fa5219760ef0fa3b26c95ebe40916f0ed2881a6491fce36944398d4c7"
ANCHOR_SHA256 = "96b2f1874d80a96e4e4443466a80110262c4665ee99611545bc36a1a2f60360c"
ROOT_EXPRESSION = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
DENOMINATOR = "ee9b5029b7cb4a820132e16aeeb1a5c6e304e81bb8624f0f931aee9547cb9bcd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_HALTING_SHA256 = "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de"
MATHLIB_HALTING_BLOB = "0834371356762db805d37208b9cf8a1fc0efd217"
LEAN_OUTPUT_SHA256 = "5d685af0e88bac202d4ed89b812359274bfb4c71e875d2f8e1a01eede57c33df"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def acyclic(edges: list[dict], name: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for row in edges:
        adjacency.setdefault(row["from"], []).append(row["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"{name} cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency.get(node, []):
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        visit(node)


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    recipes = load("validation-specs.json")
    instance = load("instance.json")

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert recipes["schema_version"] == "stage1-validation-specs/1.0"
    assert {registry["item_id"], bundle["item_id"], recipes["item_id"]} == {ITEM}
    assert {registry["theorem_id"], bundle["theorem_id"], recipes["theorem_id"]} == {THEOREM}
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0741-OBLIGATIONS-v1"
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256

    target_manifest = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )
    target = next(
        row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM
    )
    assert target["execution_rank"] == 1329
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0741-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0741"]
    assert item["deliverable"] == (
        "Freeze the obligation registry and typed proof/provenance/workflow graphs."
    )
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/THM-M-0741/{name}" for name in actual_files
    }

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 19
    assert registry["root_obligation_id"] == bundle["root_node_id"] == "M0741-ROOT"
    required_obligation = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility",
        "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    }
    for row in rows:
        assert set(row) == required_obligation
        assert row["machine_eligibility"] in {
            "required", "not_applicable", "informational"
        }
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        assert row["kind"] in {
            "root", "definition", "normalization", "reduction", "branch",
            "construction", "bridge", "core_lemma", "computation",
            "certificate", "transport", "terminal",
        }
        assert row["root_relevant"] is True
        has_any_exclusion = (
            row["machine_eligibility"] != "required"
            or row["human_source_eligibility"] != "required"
            or row["readable_eligibility"] != "required"
        )
        if has_any_exclusion:
            assert row["exclusion_reason"]
        else:
            assert row["exclusion_reason"] is None
    assert {
        row["obligation_id"] for row in rows
        if row["terminal_proof_body_id"] and "ComputablePred.halting_problem" in row["terminal_proof_body_id"]
    } == {"M0741-X-FIXED-HALTING"}

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility",
        "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    )
    projection = [{key: row[key] for key in fields} for row in rows]
    denominator = canonical_digest(projection)
    assert denominator == DENOMINATOR
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
    assert instance["obligation_registry_hash"] == "sha256:" + denominator
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
    assert set(registry["layer_exclusions"]) == {
        "additional_representative_symmetry_or_order_normalization",
        "additional_root_case_splits",
        "external_computation",
    }
    assert all(
        value["status"] == "not_applicable_pending_independent_approval"
        and value["reason"]
        for value in registry["layer_exclusions"].values()
    )
    status = registry["status_observed_after_freeze"]
    assert status["accepted_closed_obligations"] == []
    assert status["accepted_root_machine_debt"] == "M3"
    assert "below E1" in status["candidate_route"]

    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt",
        "evidence_ids", "source_crosswalk_id", "provenance_id",
        "foundation_profile", "tcb_profile", "computation_record", "step_budget",
        "semantic_step_ledger", "public_readable_target", "validation_spec_id",
        "status_boundary", "task_ids", "owned_sources", "owner", "reviewer",
        "validity",
    }
    nodes = bundle["nodes"]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    allowed_external_premises = {"frozen-formal-context", "pinned-mathlib-source"}
    for node in nodes:
        assert set(node) == required_node
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0741-")
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {
            "M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"
        }
        assert node["machine_debt"] not in {"M0-L", "M0-W", "M0-P", "M1", "M2"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
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
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0741/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validation_spec_id"] == "VAL-M0741-OBLIGATION-BUNDLE"
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert "no m0" in node["status_boundary"].lower()
        assert node["task_ids"] and node["task_ids"][0] == ITEM
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | allowed_external_premises

    allowed_edges = {
        "proof_requires", "composes", "logical_decomposition",
        "expository_decomposition", "source_map",
        "provenance_of", "evidence_for", "trusts", "documents",
        "workflow_depends_on",
    }
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0741-STATEMENT", "S56-M-0741-ANCHOR_AUDIT", ITEM,
        "S56-M-0741-PROOF", "S56-M-0741-VALIDATION", "S56-M-0741-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph_value in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        for row in graph_value["edges"]:
            assert row["edge_id"] not in edge_ids and row["type"] in allowed_edges
            endpoints = workflow_nodes if name == "workflow" else id_set
            assert row["from"] in endpoints and row["to"] in endpoints
            if name == "workflow":
                assert row["type"] == "workflow_depends_on"
            else:
                assert row["type"] != "workflow_depends_on"
            expected_out.setdefault(row["from"], []).append(row["edge_id"])
            expected_in.setdefault(row["to"], []).append(row["edge_id"])
            edge_ids.add(row["edge_id"])
        assert graph_value["out"] == expected_out
        assert graph_value["in"] == expected_in
        if name != "proof":
            acyclic(graph_value["edges"], name)
    assert len(edge_ids) == 70

    proof_edges = {
        row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]
    }
    children: dict[str, list[str]] = {}
    for row in proof_edges.values():
        assert row["type"] in {"proof_requires", "composes"}
        reverse = proof_edges[row["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == row["edge_id"]
        assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
        assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
        if row["type"] == "proof_requires":
            children.setdefault(row["from"], []).append(row["to"])
    proof_visiting: set[str] = set()
    proof_visited: set[str] = set()

    def visit_proof(obligation: str) -> None:
        assert obligation not in proof_visiting, f"proof cycle at {obligation}"
        if obligation in proof_visited:
            return
        proof_visiting.add(obligation)
        for child in children.get(obligation, []):
            visit_proof(child)
        proof_visiting.remove(obligation)
        proof_visited.add(obligation)

    visit_proof("M0741-ROOT")
    assert proof_visited == {
        "M0741-ROOT", "M0741-N-FIXED-ZERO", "M0741-L-RESTRICT",
        "M0741-C-PAIR-ZERO", "M0741-X-FIXED-HALTING", "M0741-X-RICE",
        "M0741-B-FIXED-WITNESSES",
    }
    assert {
        (row["from"], row["type"], row["to"])
        for row in bundle["graphs"]["refinement"]["edges"]
    } == {
        ("M0741-ROOT", "expository_decomposition", "M0741-S-TARGET"),
        ("M0741-ROOT", "expository_decomposition", "M0741-S-BOUNDARY"),
        ("M0741-X-RICE", "expository_decomposition", "M0741-L-FIXED-POINT"),
        ("M0741-X-RICE", "expository_decomposition", "M0741-C-CONDITIONAL"),
        ("M0741-X-RICE", "expository_decomposition", "M0741-B-MEMBERSHIP"),
    }
    for overlay in {
        "M0741-S-TARGET", "M0741-S-BOUNDARY", "M0741-L-FIXED-POINT",
        "M0741-C-CONDITIONAL", "M0741-B-MEMBERSHIP",
    }:
        obligation = next(row for row in rows if row["obligation_id"] == overlay)
        assert obligation["machine_eligibility"] == "informational"
    assert bundle["closure_boundary"]["proof_leaf_cut_set"] == [
        "M0741-C-PAIR-ZERO", "M0741-X-RICE", "M0741-B-FIXED-WITNESSES"
    ]

    certificates = {
        row["parent_obligation_id"]: row
        for row in bundle["composition_certificates"]
    }
    assert set(children) == set(certificates)
    assert set(certificates) == {
        "M0741-ROOT", "M0741-N-FIXED-ZERO", "M0741-L-RESTRICT",
        "M0741-X-FIXED-HALTING",
    }
    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"] for row in rows
    }
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {
            child: fingerprints[child] for child in children[parent]
        }
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
    assert bundle["unverified_decomposition_plans"] == []
    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M0741-X-FIXED-HALTING", "M0741-X-SOURCE", "M0741-S-FOUNDATION",
        "M0741-X-PROVENANCE", "M0741-X-TRUST", "M0741-X-READABLE",
        "M0741-X-WORKFLOW",
    ]

    assert len(recipes["recipes"]) == 1
    recipe = recipes["recipes"][0]
    assert recipe["recipe_id"] == "VAL-M0741-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0741/check_obligation_tree.py"
    ]
    assert recipe["env_allowlist"] == {} and recipe["timeout_seconds"] == 240
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == id_set
    assert set(recipe["covered_declarations"]) == {
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable",
        "ComputablePred.rice", "ComputablePred.halting_problem",
        "Stage1Instances.THM_M_0741.ObligationTree.pairZeroEmbedding_computable",
        "Stage1Instances.THM_M_0741.ObligationTree.pairToFixedRestriction_of_embedding",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedInputReduction_of_restriction",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedZeroWitnessPackage",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedInputZeroUndecidable_of_rice",
        "Stage1Instances.THM_M_0741.ObligationTree.root_of_reduction_and_fixedInput",
    }

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    halting_path = MATHLIB / "Mathlib/Computability/Halting.lean"
    assert sha256(halting_path) == MATHLIB_HALTING_SHA256
    assert output(
        "git", "rev-parse", "HEAD:Mathlib/Computability/Halting.lean", cwd=MATHLIB
    ) == MATHLIB_HALTING_BLOB
    halting = halting_path.read_text(encoding="utf-8")
    for marker in (
        "theorem rice (C : Set (ℕ →. ℕ))",
        "fixed_point₂",
        "Partrec.cond",
        "by_cases H : eval c ∈ C",
        "theorem halting_problem (n) : ¬ComputablePred fun c => (eval c n).Dom",
        "| h => rice { f | (f n).Dom } h Nat.Partrec.zero Nat.Partrec.none trivial",
    ):
        assert marker in halting, marker

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|extern|"
        r"native_decide|TODO|FIXME)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "import Statement",
        "def FixedInputReduction : Prop",
        "def RiceBridge : Prop",
        "theorem pairZeroEmbedding_computable",
        "theorem pairToFixedRestriction_of_embedding",
        "theorem fixedInputReduction_of_restriction",
        "theorem fixedZeroWitnessPackage",
        "theorem fixedInputZeroUndecidable_of_rice",
        "theorem root_of_reduction_and_fixedInput",
        "#print axioms ComputablePred.rice",
        "#print axioms root_of_reduction_and_fixedInput",
    ):
        assert marker in source, marker

    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0741-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
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
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    normalized = re.sub(r"\s+", " ", lean.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 7
    assert "propext, Quot.sound" in normalized
    assert "sorryAx" not in lean.stdout and "declaration uses 'sorry'" not in lean.stdout
    for declaration in (
        "ComputablePred.rice", "ComputablePred.halting_problem",
        "pairZeroEmbedding_computable", "pairToFixedRestriction_of_embedding",
        "fixedInputReduction_of_restriction", "fixedZeroWitnessPackage",
        "fixedInputZeroUndecidable_of_rice", "root_of_reduction_and_fixedInput",
    ):
        assert declaration in lean.stdout

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = load("obligation-tree-receipt.json")
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids)
        assert receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["substantive_ledger_step_count"] == len(step_ids)
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
            "H": "H1", "M": "M3", "R": "R4"
        }
        assert receipt["audit_complete"] is False
        assert receipt["theorem_complete"] is False
        packet_path = ROOT / ".stage1-worker-selftest.json"
        if packet_path.exists():
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            assert set(packet) == {
                "item_id", "changed_paths", "commands", "output_summary",
                "base_revision", "known_failures", "state",
            }
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["changed_paths"] == receipt["changed_paths"]
            assert packet["known_failures"] == receipt["known_failures"]
            assert packet["commands"] and packet["output_summary"].startswith("PASS:")

    print(
        f"PASS THM-M-0741 obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(
        "Lean: four conditional compositions elaborate at the exact target; "
        "no placeholders; imported bodies remain proof-phase candidates"
    )
    print("accepted root remains H1/M3/R4; accepted obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
