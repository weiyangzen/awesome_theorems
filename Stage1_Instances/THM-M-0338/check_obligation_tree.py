#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0338 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == graphs["item_id"] == specs["item_id"] == "S56-M-0338-OBLIGATION_TREE"
assert reg["theorem_id"] == graphs["theorem_id"] == specs["theorem_id"] == "THM-M-0338"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 16 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
assert reg["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
nodes = graphs["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
assert all(0 < n["step_budget"] <= 100 for n in nodes)
assert all({"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys() for n in nodes)
allowed = {"proof_requires", "composes", "source_map", "provenance_of", "trusts", "workflow_depends_on"}
edge_ids = set()
for graph in graphs["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in graphs["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reciprocal = proof[edge["reciprocal_edge_id"]]
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires": children.setdefault(edge["from"], []).append(edge["to"])
def visit(node, path):
    assert node not in path
    for child in children.get(node, []): visit(child, path | {node})
visit("M0338-ROOT", set())
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert graphs["closure_boundary"]["root_closed"] is False and graphs["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_components" in lean and "#print axioms" in lean
print(f"PASS THM-M-0338 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); exact existence, paving/MSS, source, and trust leaves remain open")
