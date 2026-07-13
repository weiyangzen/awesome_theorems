#!/usr/bin/env python3
"""Fail-closed structural and optional Lean validation for THM-M-0814 obligations."""

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
ITEM = "S56-M-0814-OBLIGATION_TREE"
THEOREM = "THM-M-0814"
ROOT_ID = "M0814-ROOT"
RANK = 1373
BASE_REVISION = "27400857bccc93638c97e9c65859ddf5d5b5f4da"
BASE_TREE = "3762537e0e5ae46cd70b086da49a69e2fd7b275c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
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
    "proof_requires", "composes", "logical_decomposition", "source_map", "transports",
    "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on",
}
CHECKED_DECLARATIONS = {"cutCertificate_compose", "compose_root", "root_of_terminal"}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


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
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0814-obligation-") as temporary:
        temp = Path(temporary)
        env = {**os.environ, "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"}
        statement = subprocess.run(
            [lean_bin, "--trust=0", "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=HERE,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_bin, "--trust=0", str(HERE / "ObligationTree.lean")],
            cwd=HERE,
            env={**env, "LEAN_PATH": f"{temp}:{lean_path}"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    assert "Declarations are sorry-free!" in obligation.stdout
    assert "sorryAx" not in obligation.stdout
    for name in CHECKED_DECLARATIONS:
        assert f"THM_M_0814_Obligations.{name}'" in obligation.stdout
    assert "propext" in obligation.stdout
    assert "Classical.choice" in obligation.stdout
    assert "Quot.sound" in obligation.stdout
    return obligation.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-lean", action="store_true")
    parser.add_argument("--worker-packet", action="store_true")
    args = parser.parse_args()

    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    receipt = load(HERE / "obligation-tree-receipt.json")

    expected = build_obligation_artifacts.build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": RANK,
        "phase": "obligation_tree", "layer": 3, "state": "[ ]",
        "depends_on": ["S56-M-0814-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0814-ANCHOR_AUDIT")
    assert predecessor["state"] in {"[_]", "[x]"}
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 33
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    assert all(set(row) == REGISTRY_FIELDS for row in rows)
    for row in rows:
        excluded = any(row[field] != "required" for field in (
            "machine_eligibility", "human_source_eligibility", "readable_eligibility"
        ))
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert set(row["exclusion_reason"]) == {"code", "justification", "approval"}
            assert "pending" in row["exclusion_reason"]["approval"]
    fields = tuple(registry["canonical_projection_fields"])
    projection = [{field: row[field] for field in fields} for row in rows]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    for eligibility, key in (("machine_eligibility", "required_machine"), ("human_source_eligibility", "required_human_source"), ("readable_eligibility", "required_readable")):
        assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert registry["append_only_delta"] == []
    assert registry["layer_exclusions"]["external_computation"]["status"].endswith("pending_independent_approval")
    observed = registry["status_observed_after_freeze"]
    assert observed["candidate_machine_classification"] == "M3_no_exact_proof_candidate"
    assert observed["candidate_closure_credit"] is False
    assert observed["accepted_closed_obligations"] == []
    assert observed["root_machine_debt"] == "M3"

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["node_id"] == f"{THEOREM}-{node['obligation_id'].removeprefix('M0814-')}"
        assert node["human_debt"] == "H1" and node["machine_debt"] in {"M3", "M4"}
        assert node["readability_debt"] == "R4" and node["evidence_ids"] == []
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
        for step in ledger:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in step_ids and step["premise_ids"] and step["inference"]
            assert step["source_locator"] and step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        path, anchor = node["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        assert f"### {anchor}" in readable
        assert node["validity"]["revocation_state"] == "not-accepted"
        assert node["task_ids"] == [ITEM]
    for node in nodes:
        for step in node["semantic_step_ledger"]:
            assert set(step["premise_ids"]) <= id_set | step_ids | {"frozen-formal-context"}

    assert bundle["root_node_id"] == f"{THEOREM}-ROOT"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    workflow_nodes = set(bundle["workflow_task_nodes"])
    edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        expected_in: dict[str, list[str]] = {}
        expected_out: dict[str, list[str]] = {}
        endpoints = workflow_nodes if name == "workflow" else id_set
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids and edge["type"] in ALLOWED_EDGES
            assert edge["from"] in endpoints and edge["to"] in endpoints
            if name == "workflow":
                assert edge["type"] == "workflow_depends_on"
            else:
                assert edge["type"] != "workflow_depends_on"
            expected_out.setdefault(edge["from"], []).append(edge["edge_id"])
            expected_in.setdefault(edge["to"], []).append(edge["edge_id"])
            edge_ids.add(edge["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in
        directional = [edge for edge in graph["edges"] if edge["type"] not in {"composes", "logical_decomposition"} or name != "proof"]
        if name != "proof":
            check_acyclic(directional)

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    reverse_types: dict[str, str] = {}
    for edge in proof.values():
        assert edge["type"] in {"proof_requires", "composes", "logical_decomposition"}
        reciprocal = proof[edge["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
        assert "proof_requires" in {edge["type"], reciprocal["type"]}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
            reverse_types[edge["from"] + "\0" + edge["to"]] = reciprocal["type"]
    check_acyclic([edge for edge in proof.values() if edge["type"] == "proof_requires"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    # Boundary/foundation analysis is attached through the separate refinement graph, as required
    # by the typed-graph contract.  Check root reachability over the union of closure-affecting
    # proof requirements and logical/transport refinements without confusing support graphs with
    # proof premises.
    closure_children = {parent: list(child_ids) for parent, child_ids in children.items()}
    for edge in bundle["graphs"]["refinement"]["edges"]:
        if edge["type"] in {"logical_decomposition", "transports"}:
            closure_children.setdefault(edge["from"], []).append(edge["to"])
    closure_reachable: set[str] = set()

    def reach_closure(node: str) -> None:
        if node in closure_reachable:
            return
        closure_reachable.add(node)
        for child in closure_children.get(node, []):
            reach_closure(child)

    reach_closure(ROOT_ID)
    required_machine = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"}
    assert required_machine <= closure_reachable
    assert len(reachable) == 21

    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == {"M0814-ROOT", "M0814-T-ASSEMBLE", "M0814-T-CUT-CERT"}
    statement_fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == statement_fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {child: statement_fingerprints[child] for child in children[parent]}
        assert certificate["checked_declaration"].rsplit(".", 1)[-1] in CHECKED_DECLARATIONS
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
        assert certificate["introduces_undeclared_premises"] is False
        assert all(reverse_types[parent + "\0" + child] == "composes" for child in children[parent])
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(children) - set(certificates)
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert "exact Lean abstract-child harness" in plan["required_future_certificate"]
        assert all(reverse_types[parent + "\0" + child] == "logical_decomposition" for child in children[parent])

    source_edges = bundle["graphs"]["provenance"]["edges"]
    for row in rows:
        identifier = row["obligation_id"]
        if identifier != "M0814-X-SOURCE" and row["human_source_eligibility"] == "required":
            assert any(edge["from"] == identifier and edge["type"] == "source_map" and edge["to"] == "M0814-X-SOURCE" for edge in source_edges)
    boundary = bundle["closure_boundary"]
    assert boundary["closed_obligations"] == instance["accepted_proof_state"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["obligation_registry_hash"] == f"sha256:{denominator}"
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    recipes = specs["recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {build_obligation_artifacts.STRUCTURE_RECIPE, build_obligation_artifacts.LEAN_RECIPE}
    for recipe in recipes:
        assert recipe["cwd"] == "." and isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["timeout_seconds"] > 0 and recipe["coverage_boundary"]
        assert set(recipe["covered_obligation_ids"]) <= id_set
    structural = next(recipe for recipe in recipes if recipe["recipe_id"] == build_obligation_artifacts.STRUCTURE_RECIPE)
    assert set(structural["covered_obligation_ids"]) == id_set and structural["covered_declarations"] == []
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"] == build_obligation_artifacts.LEAN_RECIPE)
    assert {name.rsplit(".", 1)[-1] for name in lean_recipe["covered_declarations"] if "_Obligations." in name and name.rsplit(".", 1)[-1] in CHECKED_DECLARATIONS} == CHECKED_DECLARATIONS

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    code = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    code = re.sub(r"^.*(?:assert_no_sorry|#print sorries).*$", "", code, flags=re.MULTILINE)
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|^\s*(?:axiom|constant|unsafe|opaque)\b", re.MULTILINE)
    assert forbidden.search(code) is None
    for name in CHECKED_DECLARATIONS:
        assert f"theorem {name}" in source
        assert f"assert_no_sorry {name}" in source
        assert f"#print axioms {name}" in source

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["canonical_obligation_ids"] == ids
    assert receipt["diff_summary"]
    assert receipt["lean_output_sha256"] == "e710c84702ca97b604e3d95424ea3e9ca0f43e1665df5d0468ba5adbb127322a"
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM}/{name}" for name in (
            "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
            "instance.json",
            "obligation-registry.json", "obligation-tree-receipt.json",
            "obligation-tree-validation.md", "obligation-tree.md", "typed-graphs.json",
            "validation-specs.json",
        )
    ]
    assert receipt["changed_paths"] == expected_changed
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM}/{name}" for name in actual_files
    }
    if args.worker_packet:
        packet = load(ROOT / ".stage1-worker-selftest.json")
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = output("git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json"))
        actual_changed = {line[3:] if line[:2] == "??" else line[2:].lstrip() for line in status.splitlines()}
        assert actual_changed == set(expected_changed)

    print(f"PASS THM-M-0814 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print("root closure: open (H1/M3/R4); accepted closed obligations: 0")
    if args.run_lean:
        lean_output = run_lean()
        print(f"Lean composition: pass and no sorryAx; output sha256 {hashlib.sha256(lean_output.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
