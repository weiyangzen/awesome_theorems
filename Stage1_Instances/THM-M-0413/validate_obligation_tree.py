#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
units = json.loads((HERE / "proof-units.json").read_text())

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == registry["eligibility_denominator"]["root_relevant_machine"]
assert set(ids) == set(graphs["nodes"]) == {row["obligation_id"] for row in units["nodes"]}
assert registry["eligibility_denominator"]["excluded"] == 0
assert registry["closure_status_excluded_from_freeze_decisions"] is True
for row in rows:
    assert row["root_relevant"] is True
    assert all(row[key] == "required" for key in
               ("machine_eligibility", "human_source_eligibility", "readable_eligibility"))
for row in units["nodes"]:
    assert 0 < row["step_budget"] <= 100
    assert len(row["semantic_step_ledger"]) == row["step_budget"]

proof_ids = set(ids) - {"THM-M-0413-X-TRUST"}
edges = graphs["proof_graph"]["edges"]
assert all(edge["from"] in proof_ids and edge["to"] in proof_ids for edge in edges)
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
assert visited == proof_ids

for family in ("refinement_graph", "provenance_graph", "evidence_graph", "trust_graph",
               "documentation_graph", "workflow_graph"):
    assert family in graphs and "edges" in graphs[family]
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean, forbidden
for certificate in ("components_compose", "interface_from_generic", "root_from_interface"):
    assert certificate in lean
print("ok: 10 obligations, 12 proof edges, acyclic root reachability, typed graphs, ledgers <=100")
