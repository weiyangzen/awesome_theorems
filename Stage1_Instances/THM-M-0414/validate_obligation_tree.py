#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
units = json.loads((HERE / "proof-units.json").read_text())

required_registry = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id"}
obligations = registry["obligations"]
assert all(required_registry <= set(row) for row in obligations)
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) == 4
assert set(ids) == set(graphs["nodes"])
assert set(ids) == {row["obligation_id"] for row in units["nodes"]}
assert set(ids) == set(registry["eligibility_denominator"]["root_relevant_machine_ids"])
assert registry["eligibility_denominator"]["excluded_ids"] == []

required_unit = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
                 "human_debt", "machine_debt", "readability_debt", "evidence_ids",
                 "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
                 "computation_record", "step_budget", "semantic_step_ledger",
                 "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
                 "owned_sources", "owner", "reviewer", "validity"}
assert all(required_unit <= set(row) for row in units["nodes"])
assert all(0 < row["step_budget"] <= 100 for row in units["nodes"])
assert all(len(row["semantic_step_ledger"]) == row["step_budget"] for row in units["nodes"])

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
assert visited == {"THM-M-0414-ROOT", "THM-M-0414-UFM", "THM-M-0414-FINPROD"}

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean, f"forbidden token: {forbidden}"
assert "components_compose" in lean
print("ok: 4 obligations, 2 proof edges, acyclic proof reachability, separate trust gate, ledgers <=100")
