#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
nodes_doc = json.loads((HERE / "obligation-nodes.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

required_registry = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
required_node = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}

assert registry["theorem_id"] == nodes_doc["theorem_id"] == graphs["theorem_id"] == "THM-M-0392"
rows = registry["obligations"]
assert all(required_registry <= set(row) for row in rows)
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 8
assert registry["canonical_root"] == "M0392-ROOT"
assert registry["eligibility_denominator"] == {
    "root_relevant_machine": 8, "root_relevant_human_source": 8,
    "root_relevant_readable": 8, "excluded": 0,
}
assert all(row["root_relevant"] and row["machine_eligibility"] == "required" for row in rows)
assert all(row["exclusion_reason"] is None for row in rows)

nodes = nodes_doc["nodes"]
assert all(required_node <= set(row) for row in nodes)
assert {row["obligation_id"] for row in nodes} == set(ids) == set(graphs["nodes"])
assert all(row["node_id"] == "THM-M-0392-" + row["obligation_id"].removeprefix("M0392-") for row in nodes)
assert all(0 < row["step_budget"] <= 100 for row in nodes)
assert all(len(row["semantic_step_ledger"]) == row["step_budget"] for row in nodes)
for row in nodes:
    for step in row["semantic_step_ledger"]:
        assert {"premises", "inference", "output", "outgoing_use"} <= set(step)

allowed_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(graphs["graphs"]) == allowed_graphs
for graph_name in ("proof", "refinement"):
    for edge in graphs["graphs"][graph_name]:
        assert edge["from"] in ids and edge["to"] in ids

children = {}
for edge in graphs["graphs"]["proof"]:
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting, f"proof dependency cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit(registry["canonical_root"])
assert visited == set(ids)

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean
assert registry["theorem_complete"] is False and registry["audit_complete"] is False
print("obligation_tree: ok (8 required obligations; 7 typed graphs; DAG and ledgers validated)")
