#!/usr/bin/env python3
"""Validate the frozen THM-M-0389 registry and typed graph bundle."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
units = json.loads((HERE / "proof-units.json").read_text())

obligations = registry["obligations"]
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) == 16
assert set(ids) == set(graphs["nodes"])
assert set(ids) == {row["obligation_id"] for row in units["nodes"]}
assert registry["canonical_root"] in ids
denominator = registry["eligibility_denominator"]
assert denominator == {
    "root_relevant_machine": 16,
    "root_relevant_human_source": 16,
    "root_relevant_readable": 16,
    "excluded": 0,
}
assert registry["status_observed_at_freeze"] is False
assert all(row["root_relevant"] for row in obligations)

required_unit = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "machine_debt", "provenance_id", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id",
    "status_boundary", "task_ids", "owned_sources",
}
for row in units["nodes"]:
    assert required_unit <= set(row)
    assert 0 < row["step_budget"] <= 100
    assert len(row["semantic_step_ledger"]) == row["step_budget"]

edges = graphs["proof_graph"]["edges"]
assert all(edge["from"] in ids and edge["to"] in ids for edge in edges)
children = {}
for edge in edges:
    children.setdefault(edge["from"], []).append(edge["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)

visit(registry["canonical_root"])
assert visited == set(ids) - {"M0389-X-TRUST"}

for graph_name in ("provenance_graph", "evidence_graph", "trust_graph", "documentation_graph", "workflow_graph"):
    assert isinstance(graphs[graph_name]["edges"], list)

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean, f"forbidden token: {forbidden}"
assert "theorem root_compose" in lean
assert "#print axioms root_compose" in lean
print(f"obligation tree: ok ({len(ids)} obligations, {len(edges)} proof edges, acyclic, all ledgers <=100)")
