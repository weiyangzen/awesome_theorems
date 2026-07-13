#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0079 obligation freeze."""

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
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
receipt = json.loads((HERE / "obligation-tree-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
anchor = json.loads((HERE / "anchor-audit.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0079-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0079"
assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0079-OBLIGATIONS-v1"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
root_expression = statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert root_expression == "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
assert anchor["canonical_target_expression_sha256"] == root_expression

fields = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert {row["kind"] for row in rows} <= {
    "root", "definition", "reduction", "branch", "construction", "lemma",
    "computation", "transport", "terminal",
}
assert len(ids) == len(set(ids)) == 39
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M0079-ROOT"
assert rows[0]["statement_fingerprint"] == rows[1]["statement_fingerprint"] == "lean-expression-sha256:" + root_expression
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(
    json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [
    row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"
]
assert registry["frozen_denominators"]["required_human_source"] == [
    row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"
]
assert registry["frozen_denominators"]["required_readable"] == ids
assert set(registry["layer_applicability"]) == {
    "S_statement_foundation", "N_normalization", "B_mathematical_branch",
    "C_construction", "L_core_lemma", "X_external_computation", "T_terminal",
}
assert registry["layer_applicability"]["B_mathematical_branch"]["state"] == "not_applicable_pending_independent_approval"

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
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100
    ledger = node["semantic_step_ledger"]
    assert {"premises", "inference", "output", "source_anchors", "outgoing_use", "steps"} <= ledger.keys()
    assert 0 < len(ledger["steps"]) <= node["step_budget"]
    for step in ledger["steps"]:
        assert {"step_id", "premise_ids", "inference", "output", "source_anchors", "outgoing_use"} <= step.keys()
        assert set(step["premise_ids"]) <= set(ids)
    assert node["public_readable_target"].startswith("Stage1_Instances/THM-M-0079/obligation-tree.md#")
    assert node["validation_spec_id"] in {recipe["recipe_id"] for recipe in specs["recipes"]}
    assert node["human_debt"] == "H1" and node["readability_debt"] == "R4"
    assert node["evidence_ids"] == []
    assert node["semantic_step_ledger"]["ledger_state"] == \
        "semantic_architecture_step_frozen_not_R0_reconstruction"
    assert node["semantic_step_ledger"]["budget_semantics"].startswith(
        "Architecture split threshold only, not a verified logical-step count"
    )
    provenance_id = node["provenance_id"]
    assert provenance_id == "none" or provenance_id.startswith("repo-local:") or \
        provenance_id == "anchor-audit.json#/candidates/1:proof-substrate-pending-node-specific-provenance"
    row = next(row for row in rows if row["obligation_id"] == node["obligation_id"])
    if row["terminal_proof_body_id"]:
        assert row["terminal_proof_body_id"] in node["owned_sources"]

readable = (HERE / "obligation-tree.md").read_text().lower()
for node in nodes:
    readable_anchor = node["public_readable_target"].split("#", 1)[1]
    assert re.search(rf"^#{{1,6}} {re.escape(readable_anchor)}$", readable, flags=re.M), readable_anchor

allowed_by_graph = {
    "proof": {"proof_requires", "composes"},
    "refinement": {"expository_decomposition", "equivalent_to", "transports"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
assert set(bundle["graphs"]) == set(allowed_by_graph)
edge_ids: set[str] = set()
for graph_name, graph in bundle["graphs"].items():
    assert set(graph["out"]) == set(ids) == set(graph["in"])
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        assert edge["type"] in allowed_by_graph[graph_name]
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])

proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children: dict[str, list[str]] = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

visiting: set[str] = set()
visited: set[str] = set()


def visit(node: str) -> None:
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)


visit("M0079-ROOT")
assert visited == set(registry["frozen_denominators"]["required_machine"]) - {"M0079-S-FOUNDATION"}
assert bundle["graphs"]["evidence"]["edges"] == []
assert bundle["evidence_endpoint_policy"].startswith("Receipts are external typed objects")
for edge in bundle["graphs"]["provenance"]["edges"]:
    if edge["type"] in {"source_map", "provenance_of"}:
        assert edge["from"].startswith("M0079-X-") or edge["from"] == "M0079-A-DIRECT"
for edge in bundle["graphs"]["documentation"]["edges"]:
    assert edge["from"] == "M0079-X-DOCUMENTATION"
for edge in bundle["graphs"]["refinement"]["edges"]:
    if edge["type"] in {"equivalent_to", "transports"}:
        reverse = next(
            item for item in bundle["graphs"]["refinement"]["edges"]
            if item["edge_id"] == edge["reciprocal_edge_id"]
        )
        assert reverse["reciprocal_edge_id"] == edge["edge_id"]
        assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])

certificate_children = {
    certificate["parent_id"]: certificate["required_child_ids"]
    for certificate in bundle["composition_certificates"]
}
fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in rows}
for parent, required_children in children.items():
    assert certificate_children[parent] == required_children
for certificate in bundle["composition_certificates"]:
    parent = certificate["parent_id"]
    assert certificate["parent_statement_fingerprint"] == fingerprints[parent]
    assert certificate["required_child_statement_fingerprints"] == {
        child: fingerprints[child] for child in certificate["required_child_ids"]
    }
    if certificate["kernel_checked_interface"]:
        assert certificate["status"] == "conditional_kernel_checked"
        assert "exact Lean type ascriptions" in certificate["statement_fingerprint_binding"]
    else:
        assert certificate["status"] == "planned_source_composition_pending_exact_child_harness"
    assert "architecture identities, not elaborated Lean expression hashes" in \
        certificate["statement_fingerprint_binding"]
assert {
    certificate["parent_id"]
    for certificate in bundle["composition_certificates"]
    if certificate["kernel_checked_interface"]
} == set(bundle["closure_boundary"]["checked_conditional_interfaces"])
assert bundle["closure_boundary"]["accepted_closed_obligations"] == []
assert bundle["closure_boundary"]["remaining_root_cut_set"] == [
    "M0079-L-QUOTIENT-PRETRANSITIVE", "M0079-C-QUOTIENT-NONEMPTY",
    "M0079-C-ACTION-GENERATORS", "M0079-C-SEMIDIRECT-LABELLING",
    "M0079-L-AMBIENT-UNIQUE-LIFT", "M0079-C-CURRY-UNCURRY",
    "M0079-L-FUNCTOR-UNIQUENESS", "M0079-L-HOM-PATH",
    "M0079-C-TREE-PATHS", "M0079-C-COMPLEMENT-GENERATORS",
    "M0079-C-STABILIZER-END",
    "M0079-L-QUOTIENT-STABILIZER", "M0079-T-MULEQUIV-FREENESS",
]
assert bundle["closure_boundary"]["remaining_required_machine_assurance_frontier"] == [
    "M0079-S-FOUNDATION"
]
assert bundle["closure_boundary"]["remaining_root_critical_nonproof_gates"] == [
    "M0079-S-FOUNDATION", "M0079-X-SOURCE", "M0079-X-PROVENANCE",
    "M0079-X-TRUST", "M0079-X-DOCUMENTATION", "M0079-X-WORKFLOW",
]
assert bundle["closure_boundary"]["root_machine_classification"] == "M3"
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["audit_complete"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert receipt["item_id"] == registry["item_id"]
assert receipt["phase"] == receipt["intent"] == "obligation_tree"
assert receipt["proposed_state"] == "[_]" and receipt["verdict"] == "no_state_change"
assert receipt["accepted"] is False and receipt["content_addressed"] is False
assert receipt["registry_denominator_sha256"] == digest
assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(edge_ids)
assert receipt["accepted_closed_obligations"] == []
assert receipt["remaining_root_cut_set"] == bundle["closure_boundary"]["remaining_root_cut_set"]
assert receipt["remaining_required_machine_assurance_frontier"] == \
    bundle["closure_boundary"]["remaining_required_machine_assurance_frontier"]
assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
assert receipt["accepted_receipt_ids"] == []
assert receipt["prerequisite"] == {
    "item_id": "S56-M-0079-ANCHOR_AUDIT",
    "provisional_receipt_id": "S56-M-0079-ANCHOR-AUDIT-WORKER-20260713",
    "receipt_sha256": hashlib.sha256((HERE / "anchor-audit-receipt.json").read_bytes()).hexdigest(),
    "accepted": False,
    "boundary": "Provisional dependency input only; it supplies no accepted receipt ID or state transition.",
}
assert receipt["changed_paths"] == json.loads(
    (ROOT / ".stage1-worker-selftest.json").read_text()
)["changed_paths"]
assert receipt["first_failed_gate"] == "master acceptance of the provisional S56-M-0079-ANCHOR_AUDIT prerequisite"
assert receipt["base_revision"] == subprocess.run(
    ["git", "rev-parse", "HEAD^{commit}"], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, check=True,
).stdout.strip() == "1944ddb6f503b699293e82f18d19efe0f32b4380"
assert receipt["base_tree"] == subprocess.run(
    ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, check=True,
).stdout.strip() == "e5004bc50d7e6fae75e8332fb00748a57e3bf622"
assert receipt["canonical_obligation_ids"] == ids
assert receipt["canonical_declaration"] == "Stage1Instances.THM_M_0079.NielsenSchreierTarget"
assert receipt["canonical_expression_fingerprint"] == "sha256:" + root_expression
assert receipt["checked_conditional_interfaces"] == bundle["closure_boundary"]["checked_conditional_interfaces"]
assert receipt["composition_declarations"] == [
    "Stage1Instances.THM_M_0079.ObligationTree.quotientActionConnected_of_components",
    "Stage1Instances.THM_M_0079.ObligationTree.endSubgroupEquiv_of_components",
    "Stage1Instances.THM_M_0079.ObligationTree.quotientVertexEndFree_of_components",
    "Stage1Instances.THM_M_0079.ObligationTree.exactAssembly_of_end_packages",
    "Stage1Instances.THM_M_0079.ObligationTree.root_of_exactAssembly",
]
assert receipt["conditional_premises"] == [
    "Stage1Instances.THM_M_0079.ObligationTree.QuotientActionPretransitive",
    "Stage1Instances.THM_M_0079.ObligationTree.QuotientNonempty",
    "Stage1Instances.THM_M_0079.ObligationTree.ActionGroupoidFreeConstructor",
    "Stage1Instances.THM_M_0079.ObligationTree.ConnectedFreeEndConstructor",
    "Stage1Instances.THM_M_0079.ObligationTree.StabilizerEndConstructor",
    "Stage1Instances.THM_M_0079.ObligationTree.QuotientStabilizerIdentification",
    "Stage1Instances.THM_M_0079.ObligationTree.EndSubgroupEquivConstructor",
    "Stage1Instances.THM_M_0079.ObligationTree.MulEquivFreenessTransport",
    "Stage1Instances.THM_M_0079.ObligationTree.QuotientActionConnected",
    "Stage1Instances.THM_M_0079.ObligationTree.QuotientVertexEndFree",
    "Stage1Instances.THM_M_0079.ObligationTree.ExactAssembly",
]
assert receipt["source_revisions"]["canonical_statement_sha256"] == registry["frozen_against_statement_sha256"]
assert receipt["source_revisions"]["anchor_audit_sha256"] == registry["frozen_against_anchor_audit_sha256"]
assert receipt["source_revisions"]["nielsen_schreier_source_sha256"] == \
    anchor["candidates"][0]["file_sha256"]
bound_files = {
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
    assert receipt["source_revisions"][key] == hashlib.sha256(path.read_bytes()).hexdigest()
assert receipt["validation"]["content_addressed_receipt_ids"] == []
assert receipt["validation"]["closure_credit"] is False
assert receipt["validation_window"]["started_at"] is None
assert receipt["validation_window"]["ended_at"] is None
assert "not captured" in receipt["validation_window"]["timestamp_semantics"]
assert receipt["workspace_state"]["dirty"] is True
assert receipt["workspace_state"]["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
assert receipt["workspace_state"]["untracked_input_manifest_sha256"] is None
assert receipt["workspace_state"]["automation_lake_symlink_untracked"] is True
lake_link = LEAN_ROOT / ".lake"
assert lake_link.is_symlink()
assert receipt["workspace_state"]["automation_lake_symlink_target_sha256"] == hashlib.sha256(
    os.readlink(lake_link).encode()
).hexdigest()
assert receipt["validated_at"] is None
assert receipt["owner"] == "Stage1 integration lane"
assert receipt["revocation_state"] == "open_pending_master_review"
assert receipt["support_state"] == "worker_self_tested_pending_prerequisite_and_master_acceptance"

recipe_ids = [recipe["recipe_id"] for recipe in specs["recipes"]]
assert len(recipe_ids) == len(set(recipe_ids)) == 2
checked_interfaces = set(bundle["closure_boundary"]["checked_conditional_interfaces"])
for node in nodes:
    expected_spec = (
        "S56-M-0079-OBLIGATION-TREE-LEAN"
        if node["obligation_id"] in checked_interfaces
        else "S56-M-0079-OBLIGATION-TREE-GENERATOR-CHECK"
    )
    assert node["validation_spec_id"] == expected_spec
lean_recipe = next(
    recipe for recipe in specs["recipes"]
    if recipe["recipe_id"] == "S56-M-0079-OBLIGATION-TREE-LEAN"
)
assert set(lean_recipe["covered_obligation_ids"]) == set(
    bundle["closure_boundary"]["checked_conditional_interfaces"]
)
assert lean_recipe["covered_declarations"] == receipt["composition_declarations"]
for recipe in specs["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert recipe["cwd"] in {".", "Formalizations/Lean"}
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) <= set(ids)
    assert recipe["closure_credit"] is False

task_graph = bundle["workflow_task_graph"]
execution_dag_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
execution_dag_sha256 = hashlib.sha256(execution_dag_path.read_bytes()).hexdigest()
assert bundle["frozen_against_execution_dag_sha256"] == task_graph["authority_sha256"] == execution_dag_sha256
assert bundle["local_task_dag_projection_sha256"] == hashlib.sha256((HERE / "task-dag.json").read_bytes()).hexdigest()
authoritative_items = [
    item for item in json.loads(execution_dag_path.read_text())["items"]
    if item["theorem_id"] == "THM-M-0079"
]
local_tasks = json.loads((HERE / "task-dag.json").read_text())["tasks"]
assert [
    {"id": task["id"], "phase": task["phase"], "layer": task["layer"], "depends_on": task["depends_on"]}
    for task in local_tasks
] == [
    {"id": item["id"], "phase": item["phase"], "layer": item["layer"], "depends_on": item["depends_on"]}
    for item in authoritative_items if item["phase"] != "intake"
]
task_ids = [node["task_id"] for node in task_graph["nodes"]]
assert task_graph["nodes"] == [
    {"task_id": item["id"], "phase": item["phase"], "layer": item["layer"]}
    for item in authoritative_items
]
assert [(edge["from"], edge["to"]) for edge in task_graph["edges"]] == [
    (item["id"], dependency) for item in authoritative_items for dependency in item["depends_on"]
]
assert all(link["task_id"] in task_ids and link["obligation_id"] in ids for link in task_graph["task_obligation_links"])
assert {
    (task_id, node["obligation_id"])
    for node in nodes for task_id in node["task_ids"]
} == {(link["task_id"], link["obligation_id"]) for link in task_graph["task_obligation_links"]}


def command_output(*argv: str, cwd: Path) -> str:
    result = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    return result.stdout.strip()


def lean_check() -> str:
    lean = command_output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = command_output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0079-obligation-") as temp_dir:
        temp = Path(temp_dir)
        for name in ("Statement.lean", "ObligationTree.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        env = os.environ.copy()
        env["LEAN_PATH"] = lean_path
        statement_run = subprocess.run(
            [lean, "-o", "Statement.olean", "Statement.lean"], cwd=temp, env=env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        if statement_run.returncode:
            sys.stdout.write(statement_run.stdout)
            raise SystemExit(statement_run.returncode)
        env["LEAN_PATH"] = f"{temp}:{lean_path}"
        obligation_run = subprocess.run(
            [lean, "ObligationTree.lean"], cwd=temp, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        if obligation_run.returncode:
            sys.stdout.write(obligation_run.stdout)
            raise SystemExit(obligation_run.returncode)
    for marker in (
        "'Stage1Instances.THM_M_0079.ObligationTree.quotientActionConnected_of_components' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0079.ObligationTree.endSubgroupEquiv_of_components' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0079.ObligationTree.quotientVertexEndFree_of_components' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0079.ObligationTree.exactAssembly_of_end_packages' depends on axioms: [propext,",
        "'Stage1Instances.THM_M_0079.ObligationTree.root_of_exactAssembly' depends on axioms: [propext,",
        "Classical.choice", "Quot.sound", "def Stage1Instances.THM_M_0079.NielsenSchreierTarget",
    ):
        assert marker in obligation_run.stdout, marker
    return hashlib.sha256(obligation_run.stdout.encode()).hexdigest()

lean = (HERE / "ObligationTree.lean").read_text()
code = re.sub(r"/-.*?-/", "", lean, flags=re.S)
code = re.sub(r"--.*", "", code)
forbidden = ("s" + "orry", "a" + "dmit", "a" + "xiom ", "s" + "orryAx", "unsafe ")
assert all(token not in code for token in forbidden)
for declaration in (
    "quotientActionConnected_of_components", "quotientVertexEndFree_of_components",
    "endSubgroupEquiv_of_components",
    "exactAssembly_of_end_packages",
    "root_of_exactAssembly",
):
    assert declaration in lean
assert lean.count("#print axioms") == 5

lean_output_sha256 = lean_check()
assert receipt["lean_output_sha256"] == lean_output_sha256


print(f"PASS THM-M-0079 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print(f"Lean output sha256: {lean_output_sha256}")
print("root closure: open (M3); pinned Nielsen-Schreier candidate remains pending proof and validation acceptance")
