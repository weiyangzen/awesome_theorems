#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0653 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0653-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0653"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 14 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
assert reg["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert 0 < n["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    rev = proof[e["reciprocal_edge_id"]]
    assert (rev["from"], rev["to"]) == (e["to"], e["from"])
    assert {e["type"], rev["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting = set()
def visit(x):
    assert x not in visiting
    visiting.add(x)
    for y in children.get(x, []): visit(y)
    visiting.remove(x)
visit("M0653-ROOT")
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_directions" in lean and "#print axioms" in lean
print(f"PASS THM-M-0653 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); Beth and converse direction packages remain open")
