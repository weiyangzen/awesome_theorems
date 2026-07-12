#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0342 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == graphs["item_id"] == specs["item_id"] == "S56-M-0342-OBLIGATION_TREE"
assert registry["theorem_id"] == graphs["theorem_id"] == specs["theorem_id"] == "THM-M-0342"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == registry["root_obligation_id"]
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]
nodes = graphs["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
assert all(0 < node["step_budget"] <= 100 for node in nodes)
assert all({"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys() for node in nodes)
required_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow", "source"}
assert set(graphs["graphs"]) == required_graphs
allowed = {"proof_requires", "composes", "refines_to", "provenance_of", "evidence_recorded_by", "trusts", "documented_by", "workflow_depends_on", "source_map"}
edge_ids = set()
for graph in graphs["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {edge["edge_id"]: edge for edge in graphs["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reciprocal = proof[edge["reciprocal_edge_id"]]
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
def visit(node, path):
    assert node not in path
    for child in children.get(node, []):
        visit(child, path | {node})
visit("M0342-ROOT", set())
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert graphs["closure_boundary"]["root_closed"] is False and graphs["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_exact_norm_anchor" in lean and "#print axioms" in lean
print(f"PASS THM-M-0342 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M2); proof acceptance, source, trust, provenance, and documentation gates remain open")
