#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
registry = json.loads((ROOT / "obligation-registry.json").read_text())
graphs = json.loads((ROOT / "typed-graphs.json").read_text())

statement_source = (ROOT / "Statement.lean").read_text()
harness_source = (ROOT / "ObligationTree.lean").read_text()
exact_body = """∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
        ContinuousOn f K → Set.MapsTo f K K →
          ∃ x : E, x ∈ K ∧ f x = x"""
assert exact_body in statement_source and exact_body in harness_source

assert registry["item_id"] == graphs["item_id"] == "S56-M-0318-OBLIGATION_TREE"
obligations = registry["obligations"]
ids = [item["obligation_id"] for item in obligations]
assert len(ids) == len(set(ids))
assert ids == registry["frozen_denominators"]["inventory"]
digest = hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest()
assert digest == registry["frozen_denominators"]["inventory_sha256"]

required_registry_fields = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
for item in obligations:
    assert set(item) == required_registry_fields

required_node_fields = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
nodes = graphs["nodes"]
node_ids = {node["node_id"] for node in nodes}
assert len(node_ids) == len(nodes)
assert {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert set(node) == required_node_fields
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100

allowed_edges = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
for graph in graphs["graphs"].values():
    for edge in graph["edges"]:
        assert edge["type"] in allowed_edges
        assert edge.get("reciprocal") is True

proof_edges = graphs["graphs"]["proof"]["edges"]
adj = {}
for edge in proof_edges:
    if edge["type"] == "proof_requires":
        assert edge["from"] in node_ids and edge["to"] in node_ids
        adj.setdefault(edge["from"], []).append(edge["to"])

seen, active = set(), set()
def visit(node):
    assert node not in active, "cycle in proof_requires graph"
    if node in seen:
        return
    active.add(node)
    for child in adj.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)

visit("THM-M-0318-ROOT")
assert set(graphs["root_reachability"]["proof_required_nodes"]) <= seen
assert graphs["theorem_complete"] is False
assert registry["theorem_complete"] is False
print(f"obligation tree valid: {len(ids)} obligations, {len(nodes)} typed nodes, digest {digest}")
