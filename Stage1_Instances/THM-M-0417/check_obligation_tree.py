#!/usr/bin/env python3
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
nodes_doc = json.loads((HERE / "obligation-nodes.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-recipes.json").read_text())

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

assert {registry["theorem_id"], nodes_doc["theorem_id"], graphs["theorem_id"], recipes["theorem_id"]} == {"THM-M-0417"}
rows = registry["obligations"]
assert all(required_registry <= set(row) for row in rows)
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 9
assert registry["canonical_root"] == "M0417-ROOT"
assert registry["status_observed_at_freeze"] is False
assert registry["eligibility_denominator"] == {"root_relevant_machine": 9, "root_relevant_human_source": 9, "root_relevant_readable": 9, "excluded": 0}
assert all(row["root_relevant"] and row["machine_eligibility"] == "required" for row in rows)
assert all(row["exclusion_reason"] is None for row in rows)

nodes = nodes_doc["nodes"]
assert all(required_node <= set(row) for row in nodes)
assert {row["obligation_id"] for row in nodes} == set(ids) == set(graphs["nodes"])
assert all(0 < row["step_budget"] <= 100 for row in nodes)
assert all(len(row["semantic_step_ledger"]) == row["step_budget"] for row in nodes)
for row in nodes:
    for step in row["semantic_step_ledger"]:
        assert {"step_id", "premises", "inference", "output", "outgoing_use"} <= set(step)
        assert "intermediate" not in step["output"]
        assert "frozen semantic transition" not in step["inference"]

assert set(graphs["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
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

aliases = registry["aliases_and_non_denominator_surfaces"]
assert len(aliases) == 4
assert all(alias["canonical_obligation_id"] in ids for alias in aliases)
assert len({row["terminal_proof_body_id"] for row in rows if row["terminal_proof_body_id"]}) == 2

recipe_ids = {recipe["recipe_id"] for recipe in recipes["recipes"]}
assert recipe_ids == {"recipe:M0417-obligation-tree-lean", "recipe:M0417-obligation-tree-structure"}
assert all(recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0 for recipe in recipes["recipes"])

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean
assert registry["theorem_complete"] is False and registry["audit_complete"] is False
print("obligation_tree: ok (9 required obligations; 0 exclusions; 7 typed graphs; DAG, recipes, aliases, and ledgers validated)")
