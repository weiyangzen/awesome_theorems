#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0663 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0663-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0663"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 14 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
assert reg["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires": children.setdefault(edge["from"], []).append(edge["to"])
visiting = set()
def visit(node):
    assert node not in visiting
    visiting.add(node)
    for child in children.get(node, []): visit(child)
    visiting.remove(node)
visit("M0663-ROOT")
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_partition_package" in lean and "#print axioms" in lean
print(f"PASS THM-M-0663 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); local behavior, finiteness, source, and foundation packages remain open")
