#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0088 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0088-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0088"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest()

obligations = registry["obligations"]
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] in ids
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
canonical = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids

nodes = bundle["nodes"]
assert {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert node["step_budget"] <= 100
    assert isinstance(node["semantic_step_ledger"], dict)
    assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
    assert node["validation_spec_id"] == "VAL-" + node["obligation_id"]
    assert bundle["item_id"] in node["task_ids"]

edge_ids = set()
for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"):
    graph = bundle["graphs"][name]
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids and edge["from"] != edge["to"]
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]

proof_edges = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
requires = [edge for edge in proof_edges.values() if edge["type"] == "proof_requires"]
for edge in requires:
    inverse = proof_edges[edge["reciprocal_edge_id"]]
    assert inverse["type"] == "composes" and inverse["from"] == edge["to"] and inverse["to"] == edge["from"]
    assert inverse["reciprocal_edge_id"] == edge["edge_id"]

children = {}
for edge in requires:
    children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit(registry["root_obligation_id"])
assert {"M0088-C-PREIMAGE", "M0088-L-RIGHT", "M0088-L-LEFT"}.issubset(visited)

recipes = specs["recipes"]
assert {r["obligation_id"] for r in recipes} == set(ids)
for recipe in recipes:
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["obligation_id"] in recipe["covered_obligation_ids"]

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "yonedaEmbedding_of_inverseLaws" in lean and "#print axioms" in lean
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
print(f"PASS THM-M-0088 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); preimage and inverse-law leaves remain M4")
