#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for the THM-M-0958 tree freeze."""

from __future__ import annotations

import hashlib
import importlib.util
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
ITEM = "S56-M-0958-OBLIGATION_TREE"
THEOREM = "THM-M-0958"
REGISTRY_ID = "THM-M-0958-OBLIGATIONS-v1"
BASE_REVISION = "4a10a7a4ddff88e302d5a303b16dd687d9468f63"
BASE_TREE = "730de242597680b39a7087d3204dfd1e6c41c60e"
STATEMENT_SHA256 = "765d13f4b2fc0bc8bdf0a1211039b62ed6269148819857795aac0c7a42dc40e6"
STATEMENT_JSON_SHA256 = "2e48944da988922ac8b4c9a0b56f13795c6dad8536464d29f64e449ed6920500"
ANCHOR_SHA256 = "eba38a4e3bb2530ffb45bc9560be6b667823a4b3ff9e19fdedc802fc6190224d"
ROOT_EXPRESSION = "bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BEHREND_SHA256 = "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65"
BEHREND_BLOB = "7d3eb0e603040dcd72fe35e39c82f4d615b3e254"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}
EXPECTED_IDS = [
    "M0958-ROOT", "M0958-S-INTERFACE", "M0958-S-DEFINITIONS", "M0958-S-BOUNDARY",
    "M0958-S-WITNESS-TRANSPORT", "M0958-S-ROTH-TRANSPORT", "M0958-S-FOUNDATION",
    "M0958-N-PARAMETERS", "M0958-N-DIMENSION", "M0958-N-DIGIT-RADIX",
    "M0958-N-ANNULUS-WIDTH", "M0958-N-ROUNDING", "M0958-N-THRESHOLDS",
    "M0958-B-Y-INTEGRAL", "M0958-B-Y-FLOOR", "M0958-B-PARAMETER-MERGE",
    "M0958-C-RANDOM-VARIABLES", "M0958-L-DIGIT-MEAN", "M0958-L-DIGIT-VARIANCE",
    "M0958-L-MOMENTS", "M0958-L-CHEBYSHEV", "M0958-C-ANNULUS-PARTITION",
    "M0958-L-LARGE-ANNULUS", "M0958-C-EXTERIOR-SUBSET",
    "M0958-L-NONEXTREME-WITNESS", "M0958-L-SHORT-DIRECTION-COUNT",
    "M0958-L-HYPERPLANE-SECTION", "M0958-L-OCTANT-COORDINATES",
    "M0958-L-ANNULUS-VOLUME", "M0958-C-ROTATED-LATTICE", "M0958-L-Q-COUNT",
    "M0958-L-DISCREPANCY-INDUCTION", "M0958-B-DISCREPANCY-BASE",
    "M0958-B-DISCREPANCY-SIGNED", "M0958-B-DISCREPANCY-HALFSPACE",
    "M0958-L-SLICE-RECURRENCE", "M0958-L-VOLUME-SUM-ERROR",
    "M0958-T-DISCREPANCY-MERGE", "M0958-L-EULER-SUM", "M0958-L-SAWTOOTH",
    "M0958-L-INTEGRAL-ERROR", "M0958-L-BAD-POINT-UNION", "M0958-L-EPSILON",
    "M0958-C-DIGIT-EMBED", "M0958-L-DIGIT-INJECTIVE", "M0958-L-NO-CARRY",
    "M0958-L-PROGRESSION-FREE", "M0958-L-EMBED-RANGE", "M0958-T-FIXED-INDEX",
    "M0958-L-ASYMPTOTIC-OPTIMIZATION", "M0958-T-WITNESS", "M0958-T-ROOT-COMPOSE",
    "M0958-X-DISCREPANCY-BASE", "M0958-X-BEHREND-SUPPORT", "M0958-X-PROBABILITY",
    "M0958-X-SOURCE-ELKIN", "M0958-X-SOURCE-COPPERSMITH",
    "M0958-X-SOURCE-DISCREPANCY", "M0958-X-SOURCE-SPECIAL", "M0958-X-PROVENANCE",
    "M0958-X-EVIDENCE", "M0958-X-TRUST", "M0958-X-READABLE", "M0958-X-WORKFLOW",
]


def load(name: str) -> dict:
    path = HERE / name

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key in {name}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), name
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def acyclic(edges: list[dict], name: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        adjacency.setdefault(item["from"], []).append(item["to"])
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


def load_builder():
    path = HERE / "build_obligation_artifacts.py"
    spec = importlib.util.spec_from_file_location("m0958_obligation_builder", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    validation = load("validation-specs.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert validation["schema_version"] == "stage1-validation-specs/1.0"
    assert {registry["item_id"], bundle["item_id"], validation["item_id"]} == {ITEM}
    assert {registry["theorem_id"], bundle["theorem_id"], validation["theorem_id"]} == {THEOREM}
    assert registry["registry_id"] == bundle["registry_id"] == REGISTRY_ID
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "statement.json") == STATEMENT_JSON_SHA256
    assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
    assert registry["architecture_source_sha256"] == sha256(HERE / "ObligationTree.lean")
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0958.ElkinConstructionTarget"
    assert formal["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert anchor["canonical_target_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_statement_file_sha256"] == STATEMENT_SHA256
    decision = anchor["inventory_decision"]
    assert decision["root_machine_classification"] == "M3"
    assert decision["exact_candidate_located"] is False
    assert decision["candidate_accepted_by_master"] is False
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False

    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1492 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0958-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0958"]
    assert item["deliverable"] == "Freeze the obligation registry and typed proof/provenance/workflow graphs."

    builder = load_builder()
    expected_registry, expected_bundle, expected_validation, expected_readable = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert validation == expected_validation
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_readable

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert ids == EXPECTED_IDS and len(ids) == len(id_set) == 64
    assert registry["root_obligation_id"] == bundle["root_node_id"] == "M0958-ROOT"
    required_obligation = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    allowed_kinds = {
        "root", "definition", "normalization", "reduction", "branch",
        "construction", "bridge", "core_lemma", "computation", "certificate",
        "transport", "terminal",
    }
    for row in rows:
        assert set(row) == required_obligation
        assert row["kind"] in allowed_kinds
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
    denominator = canonical_digest([{key: row[key] for key in fields} for row in rows])
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
        ("informational_overlays", "machine_eligibility", "informational"),
    ):
        assert frozen[key] == [row["obligation_id"] for row in rows if row[field] == value]
    layers = registry["mandatory_layers"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T"}
    assert all(layers[layer] and set(layers[layer]) <= id_set for layer in layers)
    assert set(registry["layer_exclusions"]) == {
        "additional_symmetry_sign_or_representative_normalization", "external_computation",
    }
    assert all(value["status"] == "not_applicable_pending_independent_approval" and value["reason"] for value in registry["layer_exclusions"].values())
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["accepted_root_machine_debt"] == "M3"
    assert "No exact Elkin proof candidate" in observed["candidate_route"]

    nodes = bundle["nodes"]
    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger",
        "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
        "owned_sources", "owner", "reviewer", "validity",
    }
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    allowed_external = {"frozen-formal-context", "frozen-source-context"}
    for node in nodes:
        assert set(node) == required_node
        assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0958-")
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert set(step["premise_ids"]) <= id_set | allowed_external
            step_ids.add(step["step_id"])
        path, anchor_name = node["public_readable_target"].split("#", 1)
        assert path == "Stage1_Instances/THM-M-0958/obligation-tree.md"
        assert f"### {anchor_name}" in readable
        assert node["validation_spec_id"] == "VAL-" + node["obligation_id"]
        assert node["task_ids"] == [ITEM, "S56-M-0958-PROOF"]
        assert node["owner"] and node["reviewer"] and node["validity"]["review_due"]

    allowed_edges = {
        "proof_requires", "composes", "logical_decomposition", "source_map",
        "expository_decomposition", "equivalent_to", "transports", "evidence_for",
        "provenance_of", "documents", "trusts", "workflow_depends_on",
    }
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    assert workflow_nodes == {
        "S56-M-0958-STATEMENT", "S56-M-0958-ANCHOR_AUDIT", ITEM,
        "S56-M-0958-PROOF", "S56-M-0958-VALIDATION", "S56-M-0958-RELEASE",
    }
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        for item_edge in graph["edges"]:
            assert item_edge["edge_id"] not in edge_ids
            assert item_edge["type"] in allowed_edges
            endpoints = workflow_nodes if name == "workflow" else id_set
            assert item_edge["from"] in endpoints and item_edge["to"] in endpoints
            if name == "workflow":
                assert item_edge["type"] == "workflow_depends_on"
            else:
                assert item_edge["type"] != "workflow_depends_on"
            expected_out.setdefault(item_edge["from"], []).append(item_edge["edge_id"])
            expected_in.setdefault(item_edge["to"], []).append(item_edge["edge_id"])
            edge_ids.add(item_edge["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in
        if name != "proof":
            acyclic(graph["edges"], name)
    assert len(edge_ids) == 85

    proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for item_edge in proof.values():
        assert item_edge["type"] in {"proof_requires", "composes"}
        reverse = proof[item_edge["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item_edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (item_edge["to"], item_edge["from"])
        assert {item_edge["type"], reverse["type"]} == {"proof_requires", "composes"}
        if item_edge["type"] == "proof_requires":
            children.setdefault(item_edge["from"], []).append(item_edge["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit_proof(node: str) -> None:
        assert node not in visiting, f"proof cycle at {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit_proof(child)
        visiting.remove(node)
        visited.add(node)

    visit_proof("M0958-ROOT")
    assert visited == {"M0958-ROOT", "M0958-T-ROOT-COMPOSE", "M0958-T-WITNESS", "M0958-S-WITNESS-TRANSPORT"}
    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == set(children) == {"M0958-ROOT"}
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    certificate = certificates["M0958-ROOT"]
    assert certificate["required_child_ids"] == children["M0958-ROOT"]
    assert certificate["parent_statement_fingerprint"] == fingerprints["M0958-ROOT"]
    assert certificate["required_child_statement_fingerprints"] == {child: fingerprints[child] for child in children["M0958-ROOT"]}
    assert certificate["declaration"].endswith("root_of_terminal_packages")
    assert certificate["certificate_kind"] == "lean_abstract_child_harness"
    assert certificate["introduces_undeclared_premises"] is False
    assert certificate["status"] == "provisionally_elaborated_not_accepted"
    plans = bundle["unverified_decomposition_plans"]
    assert len(plans) == 13
    for plan in plans:
        assert plan["parent_obligation_id"] in id_set
        assert set(plan["planned_child_ids"]) <= id_set
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert plan["required_future_certificate"]
    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["minimal_open_machine_proof_cut_sets"] == [["M0958-T-WITNESS"]]

    recipes = validation["recipes"]
    assert len(recipes) == len(ids)
    recipe_required = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "closure_credit",
    }
    assert {recipe["recipe_id"] for recipe in recipes} == {"VAL-" + identifier for identifier in ids}
    for recipe in recipes:
        assert set(recipe) == recipe_required
        assert recipe["cwd"] == "."
        assert recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0958/check_obligation_tree.py"]
        assert recipe["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["closure_credit"] is False and len(recipe["covered_obligation_ids"]) == 1

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    behrend_path = MATHLIB / "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean"
    assert sha256(behrend_path) == BEHREND_SHA256
    assert output("git", "rev-parse", "HEAD:Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean", cwd=MATHLIB) == BEHREND_BLOB
    behrend_source = behrend_path.read_text(encoding="utf-8")
    for marker in (
        "theorem threeAPFree_image_sphere", "theorem card_sphere_le_rothNumberNat",
        "theorem exists_large_sphere", "theorem bound_aux", "theorem roth_lower_bound_explicit",
    ):
        assert marker in behrend_source

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|extern|"
        r"native_decide|TODO|FIXME|proof_wanted)\b"
    )
    assert forbidden.search(without_comments) is None
    for marker in (
        "import Statement", "def ConstructionWitnessPackage : Prop",
        "def WitnessToRootTransport : Prop", "def RootComposition : Prop",
        "theorem checkedWitnessToRootTransport", "theorem rootComposition_checked",
        "theorem root_of_terminal_packages", "#print axioms root_of_terminal_packages",
    ):
        assert marker in source

    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0958-obligation-") as temp_dir:
        statement_run = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path, "LC_ALL": "C", "TZ": "UTC"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement_run.returncode:
            sys.stdout.write(statement_run.stdout)
            raise SystemExit(statement_run.returncode)
        lean_run = subprocess.run(
            [lean_exe, "ObligationTree.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": temp_dir + ":" + lean_path, "LC_ALL": "C", "TZ": "UTC"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if lean_run.returncode:
            sys.stdout.write(lean_run.stdout)
            raise SystemExit(lean_run.returncode)
    assert "sorryAx" not in lean_run.stdout and "declaration uses 'sorry'" not in lean_run.stdout
    for declaration in (
        "checkedWitnessToRootTransport", "rootComposition_checked", "root_of_terminal_packages",
    ):
        assert declaration in lean_run.stdout

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = load("obligation-tree-receipt.json")
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["verdict"] == "no_state_change"
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["substantive_ledger_step_count"] == len(step_ids)
        assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        assert receipt["lean_output_sha256"] == hashlib.sha256(lean_run.stdout.encode()).hexdigest()
        packet_path = ROOT / ".stage1-worker-selftest.json"
        if packet_path.exists():
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["changed_paths"] == receipt["changed_paths"]
            assert packet["known_failures"] == receipt["known_failures"]
            assert packet["commands"] and packet["output_summary"].startswith("PASS:")

    print(
        f"PASS THM-M-0958 obligation tree: {len(ids)} registry records, "
        f"{len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {hashlib.sha256(lean_run.stdout.encode()).hexdigest()}")
    print("Lean: exact witness transport and conditional child-to-root composition elaborate")
    print("accepted root remains H1/M3/R4; accepted obligations 0; theorem_complete=false")


if __name__ == "__main__":
    main()
