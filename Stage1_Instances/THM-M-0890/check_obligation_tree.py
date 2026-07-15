#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-0890 obligation freeze."""

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
ITEM = "S56-M-0890-OBLIGATION_TREE"
THEOREM = "THM-M-0890"
ROOT_ID = "M0890-ROOT"
RANK = 1440
BASE_REVISION = "6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d"
BASE_TREE = "9e8c2b617c489611e447b350a4b4cf4aeff15f39"
EXPRESSION_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
STATEMENT_SHA256 = "beb6cbe0437f78f26188cc3ed1ebe82bed84d2a07f1f8ea1abd78468740a787f"
ANCHOR_SHA256 = "b922f69cb16eed05e8f29f281460a928e787619a7c7f4c923ea312a1bf098549"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "91dcc562d27a75bc4e899d96a5997f9fdf1c76c4b81c0c9a66de228d902b8ce8"
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
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
CHECKED_DECLARATIONS = {
    "maximumIndependentSetWitness_checked", "divisionFree_of_maximumEstimate",
    "assembly_of_children", "root_of_ratio_assembly", "root_of_children",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    value: dict = {}
    for key, item in pairs:
        assert key not in value, f"duplicate JSON key {key}"
        value[key] = item
    return value


def load(path: Path) -> dict:
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


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def run_lean() -> str:
    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0890-obligation-") as temporary:
        temp = Path(temporary)
        env = {**os.environ, "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"}
        statement = subprocess.run(
            [lean_bin, "--trust=0", "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=HERE,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
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
            timeout=240,
            check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    assert "Declarations are sorry-free!" in obligation.stdout
    assert "sorryAx" not in obligation.stdout
    for name in CHECKED_DECLARATIONS:
        assert f"THM_M_0890_Obligations.{name}'" in obligation.stdout
    reports = re.findall(r"depends on axioms: \[(.*?)\]", obligation.stdout, re.DOTALL)
    assert len(reports) == 5
    assert all({part.strip() for part in report.replace("\n", "").split(",")} == EXPECTED_AXIOMS for report in reports)
    return obligation.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-lean", action="store_true")
    parser.add_argument("--worker-packet", action="store_true")
    args = parser.parse_args()

    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    receipt_path = HERE / "obligation-tree-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None

    expected = build_obligation_artifacts.build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), expected):
        assert (HERE / name).read_bytes() == canonical(value), f"stale generated artifact: {name}"

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": RANK,
        "phase": "obligation_tree", "layer": 3, "state": "[ ]",
        "depends_on": ["S56-M-0890-ANCHOR_AUDIT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0890-ANCHOR_AUDIT")
    assert predecessor["state"] in {"[_]", "[x]"}
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []
    assert task_dag["accepted_states"] == []

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert sha256(HERE / "Statement.lean") == registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "anchor-audit.json") == registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256
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
    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert layers["not_applicable_layers"] == [] and all(layers[name] for name in "SNBCLXT")
    assert all(value["status"].endswith("pending_independent_approval") for value in registry["layer_exclusions"].values())
    observed = registry["status_observed_after_freeze"]
    assert observed["candidate_machine_classification"] == "M3_no_exact_proof_candidate"
    assert observed["candidate_closure_credit"] is False
    assert observed["accepted_closed_obligations"] == []
    assert observed["root_machine_debt"] == "M3"

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == id_set
    readable_path = HERE / "obligation-tree.md"
    readable = readable_path.read_text(encoding="utf-8").lower() if readable_path.exists() else ""
    step_ids: set[str] = set()
    for node in nodes:
        assert set(node) == NODE_FIELDS
        assert node["node_id"] == f"{THEOREM}-{node['obligation_id'].removeprefix('M0890-')}"
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
        path, anchor_name = node["public_readable_target"].split("#", 1)
        assert path == f"Stage1_Instances/{THEOREM}/obligation-tree.md"
        if readable:
            assert f"### {anchor_name}" in readable
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
            assert (edge["type"] == "workflow_depends_on") == (name == "workflow")
            expected_out.setdefault(edge["from"], []).append(edge["edge_id"])
            expected_in.setdefault(edge["to"], []).append(edge["edge_id"])
            edge_ids.add(edge["edge_id"])
        assert graph["out"] == expected_out and graph["in"] == expected_in
        if name != "proof":
            check_acyclic(graph["edges"])

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    reverse_types: dict[tuple[str, str], str] = {}
    for edge in proof.values():
        assert edge["type"] in {"proof_requires", "composes", "logical_decomposition"}
        reciprocal = proof[edge["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
        assert "proof_requires" in {edge["type"], reciprocal["type"]}
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
            reverse_types[(edge["from"], edge["to"])] = reciprocal["type"]
    obligation_by_id = {row["obligation_id"]: row for row in rows}
    for parent, child_ids in children.items():
        assert obligation_by_id[parent]["machine_eligibility"] == "required"
        assert all(obligation_by_id[child]["machine_eligibility"] == "required" for child in child_ids)
    check_acyclic([edge for edge in proof.values() if edge["type"] == "proof_requires"])
    reachable: set[str] = set()

    def reach(node: str) -> None:
        if node in reachable:
            return
        reachable.add(node)
        for child in children.get(node, []):
            reach(child)

    reach(ROOT_ID)
    closure_children = {parent: list(child_ids) for parent, child_ids in children.items()}
    for edge in bundle["graphs"]["refinement"]["edges"]:
        if edge["type"] in {"logical_decomposition", "transports", "equivalent_to"}:
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
    certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
    assert set(certificates) == {"M0890-ROOT", "M0890-T-ASSEMBLE", "M0890-T-DIVISION-FREE"}
    expected_certificate_declarations = {
        "M0890-ROOT": "Stage1Instances.THM_M_0890_Obligations.root_of_ratio_assembly",
        "M0890-T-ASSEMBLE": "Stage1Instances.THM_M_0890_Obligations.assembly_of_children",
        "M0890-T-DIVISION-FREE": "Stage1Instances.THM_M_0890_Obligations.divisionFree_of_maximumEstimate",
    }
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
    for parent, certificate in certificates.items():
        assert certificate["required_child_ids"] == children[parent]
        assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
        assert certificate["required_child_statement_fingerprints"] == {child: fingerprints[child] for child in children[parent]}
        assert certificate["certificate_kind"] == "lean_abstract_child_harness"
        assert certificate["status"] == "provisionally_elaborated_not_accepted"
        assert certificate["introduces_undeclared_premises"] is False
        assert certificate["checked_declaration"] == expected_certificate_declarations[parent]
        assert certificate["checked_declaration"].rsplit(".", 1)[-1] in CHECKED_DECLARATIONS
        assert all(reverse_types[(parent, child)] == "composes" for child in children[parent])
    plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
    assert set(plans) == set(children) - set(certificates)
    for parent, plan in plans.items():
        assert plan["planned_child_ids"] == children[parent]
        assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        assert all(reverse_types[(parent, child)] == "logical_decomposition" for child in children[parent])

    source_edges = bundle["graphs"]["provenance"]["edges"]
    for row in rows:
        identifier = row["obligation_id"]
        if identifier != "M0890-X-SOURCE" and row["human_source_eligibility"] == "required":
            assert any(edge["from"] == identifier and edge["type"] == "source_map" and edge["to"] == "M0890-X-SOURCE" for edge in source_edges)
    assert bundle["graphs"]["evidence"]["edges"] == []
    assert not any(edge["type"] == "evidence_for" for edge in source_edges)
    assert not any(edge["from"] == "M0890-X-PROVENANCE" and edge["type"] == "provenance_of" for edge in source_edges)
    boundary = bundle["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"

    recipes = specs["recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {build_obligation_artifacts.STRUCTURE_RECIPE, build_obligation_artifacts.LEAN_RECIPE}
    for recipe in recipes:
        assert recipe["cwd"] == "." and isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0 and recipe["timeout_seconds"] > 0
        assert set(recipe["covered_obligation_ids"]) <= id_set and recipe["coverage_boundary"]

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
    assert sha256(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert sha256(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

    for path in HERE.iterdir():
        if path.is_file():
            check_text(path)

    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["content_addressed"] is False
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["composition_certificate_count"] == len(certificates)
        assert receipt["unverified_decomposition_count"] == len(plans)
        assert receipt["canonical_obligation_ids"] == ids
        assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
        assert set(receipt["graph_names"]) == GRAPH_NAMES
        assert receipt["accepted_closed_obligations"] == receipt["accepted_receipt_ids"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        assert receipt["selftest_result"] == "pass"
        for relative, tagged_digest in receipt["source_inputs"].items():
            assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
        expected_changed = [".stage1-worker-selftest.json"] + [
            f"Stage1_Instances/{THEOREM}/{name}" for name in (
                "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
                "obligation-registry.json", "obligation-tree-receipt.json",
                "obligation-tree-validation.md", "obligation-tree.md", "typed-graphs.json",
                "validation-specs.json",
            )
        ]
        assert receipt["changed_paths"] == expected_changed
        if args.worker_packet:
            packet = load(ROOT / ".stage1-worker-selftest.json")
            assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["changed_paths"] == receipt["changed_paths"]
            assert packet["known_failures"] == receipt["known_failures"]
            assert packet["commands"] == receipt["commands_and_results"]
            status = output("git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json"))
            actual_changed = {line[3:] if line[:2] == "??" else line[2:].lstrip() for line in status.splitlines()}
            assert actual_changed == set(expected_changed)

    print(f"PASS THM-M-0890 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print(f"checked composition certificates: {len(certificates)}; unverified decompositions: {len(plans)}")
    print("root closure: open (H1/M3/R4); accepted closed obligations: 0")
    if args.run_lean:
        lean_output = run_lean()
        lean_hash = hashlib.sha256(lean_output.encode()).hexdigest()
        assert lean_hash == LEAN_OUTPUT_SHA256
        print(f"Lean composition: pass and no sorryAx; output sha256 {lean_hash}")


if __name__ == "__main__":
    main()
