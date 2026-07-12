#!/usr/bin/env python3
"""Fail-closed structural checks for THM-M-1553's frozen architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-1553-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1553"
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 14
assert registry["root_obligation_id"] == bundle["root_node_id"] == "M1553-ROOT"

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]

den = registry["frozen_denominators"]
assert den["inventory"] == ids
assert den["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert den["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert den["required_readable"] == ids
assert den["informational_overlays"] == ["M1553-X-PROVENANCE", "M1553-X-TRUST"]

nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids)
required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owner", "reviewer", "validity"}
assert all(required_node_fields <= set(n) for n in nodes)
assert all(0 < n["step_budget"] <= 100 for n in nodes)
assert all(set(n["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"} for n in nodes)

graphs = bundle["graphs"]
assert set(graphs) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = [e for graph in graphs.values() for e in graph["edges"]]
edge_ids = [e["edge_id"] for e in all_edges]
assert len(edge_ids) == len(set(edge_ids))
assert all(e["from"] in ids and e["to"] in ids and e["from"] != e["to"] for e in all_edges)
for graph in graphs.values():
    for e in graph["edges"]:
        assert e["edge_id"] in graph["out"][e["from"]]
        assert e["edge_id"] in graph["in"][e["to"]]

proof_edges = graphs["proof"]["edges"]
by_id = {e["edge_id"]: e for e in proof_edges}
requirements = [e for e in proof_edges if e["type"] == "proof_requires"]
for e in proof_edges:
    reciprocal = by_id[e["reciprocal_edge_id"]]
    assert reciprocal["reciprocal_edge_id"] == e["edge_id"]
    assert reciprocal["from"] == e["to"] and reciprocal["to"] == e["from"]
    assert {e["type"], reciprocal["type"]} == {"proof_requires", "composes"}

# Requirement graph is acyclic and every required machine node is root-reachable,
# apart from the deliberately separate release/provenance overlays.
children = {}
for e in requirements:
    children.setdefault(e["from"], []).append(e["to"])
visiting, visited = set(), set()
def walk(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        walk(child)
    visiting.remove(node); visited.add(node)
walk("M1553-ROOT")
required_machine = {r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"}
assert required_machine <= visited

closure = bundle["closure_boundary"]
assert closure["root_closed"] is False and closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M1553-B-POLYNOMIAL", "M1553-T-ZERO"]
assert registry["status_observed_after_freeze"]["closed_obligations"] == ["M1553-T-ASSEMBLE"]

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "hirotaKdVTarget_of_logDerivativeBridge" in lean and "#print axioms" in lean
print(f"PASS THM-M-1553 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); logarithmic-derivative bridge remains M4")
