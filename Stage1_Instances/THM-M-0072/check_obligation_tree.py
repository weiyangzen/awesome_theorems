#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for the THM-M-0072 obligation freeze."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
PREFIX = "M0072"
ITEM_ID = "S56-M-0072-OBLIGATION_TREE"
THEOREM_ID = "THM-M-0072"
ROOT_EXPRESSION = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*argv: str, cwd: Path) -> str:
    result = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def lean_check() -> tuple[str, str]:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0072-obligation-") as temp_dir:
        temp = Path(temp_dir)
        for name in ("Statement.lean", "ObligationTree.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        statement_run = subprocess.run(
            [lean, "-o", "Statement.olean", "Statement.lean"], cwd=temp, env=env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        if statement_run.returncode:
            sys.stdout.write(statement_run.stdout)
            raise SystemExit(statement_run.returncode)
        env["LEAN_PATH"] = f"{temp}:{lean_path}"
        obligation_run = subprocess.run(
            [lean, "ObligationTree.lean"], cwd=temp, env=env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        if obligation_run.returncode:
            sys.stdout.write(obligation_run.stdout)
            raise SystemExit(obligation_run.returncode)
        combined = statement_run.stdout + obligation_run.stdout
    required = (
        "insideMaximalConclusion",
        "assembly_of_outside_and_inside",
        "root_of_assembly",
        "root_of_outsideTransfer",
        "ThompsonTransferLemmaTarget",
    )
    assert all(name in combined for name in required)
    assert "declaration has metavariables" not in combined
    return hashlib.sha256(combined.encode()).hexdigest(), combined


def strip_lean_comments(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    return re.sub(r"--.*", "", text)


def main() -> None:
    subprocess.run(
        [sys.executable, "-B", str(HERE / "build_obligation_artifacts.py"), "--check"],
        cwd=ROOT, check=True,
    )
    registry = json.loads((HERE / "obligation-registry.json").read_text())
    bundle = json.loads((HERE / "typed-graphs.json").read_text())
    specs = json.loads((HERE / "validation-specs.json").read_text())
    statement = json.loads((HERE / "statement.json").read_text())
    anchor = json.loads((HERE / "anchor-audit.json").read_text())

    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM_ID
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM_ID
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0072-OBLIGATIONS-v1"
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["canonical_target"] == "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget"

    fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    obligations = registry["obligations"]
    ids = [row["obligation_id"] for row in obligations]
    assert len(ids) == len(set(ids)) == 28
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == f"{PREFIX}-ROOT"
    assert all(set(row) == fields for row in obligations)
    projection = [{key: row[key] for key in (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )} for row in obligations]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    assert registry["frozen_denominators"]["inventory"] == ids
    assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"]
    assert registry["frozen_denominators"]["required_human_source"] == [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"]
    assert registry["frozen_denominators"]["required_readable"] == ids
    assert set(registry["layer_applicability"]) == {
        "S_statement_foundation", "N_normalization", "B_mathematical_branch",
        "C_construction", "L_core_lemma", "X_external_computation", "T_terminal",
    }
    assert registry["layer_applicability"]["B_mathematical_branch"]["state"] == "required"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
        "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
        "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
        "reviewer", "validity",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert {node["obligation_id"] for node in nodes} == set(ids)
    recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
    markdown = (HERE / "obligation-tree.md").read_text()
    for node in nodes:
        assert required_node <= node.keys()
        assert 0 < node["step_budget"] <= 100
        ledger = node["semantic_step_ledger"]
        assert {"premises", "inference", "output", "source_anchors", "outgoing_use", "steps", "ledger_state"} <= ledger.keys()
        assert 0 < len(ledger["steps"]) <= node["step_budget"]
        for step in ledger["steps"]:
            assert {"step_id", "premise_ids", "inference", "output", "source_anchors", "outgoing_use"} <= step.keys()
            assert set(step["premise_ids"]) <= set(ids)
        assert node["human_debt"] == "H1" and node["readability_debt"] == "R4"
        assert node["evidence_ids"] == []
        assert node["validation_spec_id"] in recipe_ids
        target, anchor_name = node["public_readable_target"].split("#", 1)
        assert target == f"Stage1_Instances/{THEOREM_ID}/obligation-tree.md"
        assert f'<a id="{anchor_name}"></a>' in markdown

    allowed = {
        "proof": {"proof_requires", "composes", "logical_decomposition"},
        "refinement": {"expository_decomposition", "transports"},
        "provenance": {"source_map", "provenance_of"},
        "evidence": {"evidence_for"},
        "trust": {"trusts"},
        "documentation": {"documents"},
        "workflow": {"workflow_depends_on"},
    }
    assert set(bundle["graphs"]) == set(allowed)
    edge_ids: set[str] = set()
    for graph_name, graph in bundle["graphs"].items():
        assert set(graph["out"]) == set(ids) == set(graph["in"])
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids
            assert edge["type"] in allowed[graph_name]
            assert edge["from"] in ids and edge["to"] in ids
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            edge_ids.add(edge["edge_id"])
    assert len(edge_ids) == bundle["typed_edge_count"] == 97
    assert bundle["graphs"]["evidence"]["edges"] == []

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    checked_children: dict[str, list[str]] = {}
    dependency_children: dict[str, list[str]] = {}
    for edge in proof.values():
        if edge["type"] == "proof_requires":
            reverse = proof[edge["reciprocal_edge_id"]]
            assert reverse["type"] == "composes"
            assert reverse["reciprocal_edge_id"] == edge["edge_id"]
            assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
            checked_children.setdefault(edge["from"], []).append(edge["to"])
            dependency_children.setdefault(edge["from"], []).append(edge["to"])
        elif edge["type"] == "logical_decomposition":
            dependency_children.setdefault(edge["from"], []).append(edge["to"])
    assert len([edge for edge in proof.values() if edge["type"] == "logical_decomposition"]) == bundle["unverified_decomposition_count"] == 20

    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(oid: str) -> None:
        assert oid not in visiting
        if oid in visited:
            return
        visiting.add(oid)
        for child in dependency_children.get(oid, []):
            visit(child)
        visiting.remove(oid)
        visited.add(oid)
    visit(f"{PREFIX}-ROOT")
    assert {f"{PREFIX}-ROOT", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-OUTSIDE"} <= visited

    certificate_children = {certificate["parent_id"]: certificate["required_child_ids"] for certificate in bundle["composition_certificates"]}
    for parent, children in checked_children.items():
        assert set(certificate_children[parent]) == set(children)
    assert all(not certificate["accepted"] for certificate in bundle["composition_certificates"])
    closure = bundle["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_classification"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["remaining_root_cut_set"] == [f"{PREFIX}-T-OUTSIDE"]
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert len(bundle["harness_relationships"]) == 2
    assert all(relation["closure_credit"] is False for relation in bundle["harness_relationships"])
    assert all("pending" in relation["graph_edge_state"] or relation["graph_edge_state"] == "conditional_harness_only" for relation in bundle["harness_relationships"])

    task_graph = bundle["workflow_task_graph"]
    dag_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    assert bundle["frozen_against_execution_dag_sha256"] == task_graph["authority_sha256"] == sha256(dag_path)
    authoritative = [item for item in json.loads(dag_path.read_text())["items"] if item["theorem_id"] == THEOREM_ID]
    assert task_graph["nodes"] == [{"task_id": item["id"], "phase": item["phase"], "layer": item["layer"]} for item in authoritative]
    expected_task_edges = [(item["id"], dependency) for item in authoritative for dependency in item["depends_on"]]
    assert [(edge["from"], edge["to"]) for edge in task_graph["edges"]] == expected_task_edges
    assert all(link["obligation_id"] in ids for link in task_graph["task_obligation_links"])

    for recipe in specs["recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert set(recipe["covered_obligation_ids"]) <= set(ids)
        assert recipe["closure_credit"] is False

    lean_source = strip_lean_comments((HERE / "ObligationTree.lean").read_text())
    forbidden = re.search(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b", lean_source)
    assert forbidden is None, f"prohibited Lean construct: {forbidden.group(0)}"
    lean_hash, lean_stdout = lean_check()
    assert "depends on axioms:" in lean_stdout

    receipt_path = HERE / "obligation-tree-receipt.json"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        assert receipt["item_id"] == ITEM_ID and receipt["proposed_state"] == "[_]"
        assert receipt["accepted"] is False and receipt["content_addressed"] is False
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["lean_output_sha256"] == lean_hash
        bound_files = {
            "canonical_statement_sha256": HERE / "Statement.lean",
            "anchor_audit_sha256": HERE / "anchor-audit.json",
            "execution_dag_sha256": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
            "local_task_dag_sha256": HERE / "task-dag.json",
            "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
            "authoritative_blueprint_sha256": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
            "target_manifest_sha256": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
            "execution_skill_sha256": ROOT / "skills/execute-stage1-rev56/SKILL.md",
            "obligation_tree_lean_sha256": HERE / "ObligationTree.lean",
            "obligation_registry_file_sha256": HERE / "obligation-registry.json",
            "typed_graphs_file_sha256": HERE / "typed-graphs.json",
            "validation_specs_file_sha256": HERE / "validation-specs.json",
            "generator_sha256": HERE / "build_obligation_artifacts.py",
            "checker_sha256": HERE / "check_obligation_tree.py",
        }
        for key, path in bound_files.items():
            assert receipt["source_revisions"][key] == sha256(path)
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
        assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False

    print(f"PASS {THEOREM_ID} obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean output sha256: {lean_hash}")
    print("open root: H1/M3/R4; accepted closures 0; outside transfer branch remains required")


if __name__ == "__main__":
    main()
