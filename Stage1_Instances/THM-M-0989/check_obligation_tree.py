#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0989 frozen architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-0989-OBLIGATION_TREE"
obligations = registry["obligations"]
ids = [o["obligation_id"] for o in obligations]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] in ids
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
payload = json.dumps([{k: o[k] for k in fields} for o in obligations], sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(payload).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert {n["obligation_id"] for n in bundle["nodes"]} == set(ids)
assert {r["obligation_id"] for r in recipes["recipes"]} == set(ids)
for node in bundle["nodes"]:
    assert node["step_budget"] <= 100
    assert all(node.get(k) for k in ("semantic_step_ledger", "validation_spec_id", "status_boundary", "foundation_profile", "tcb_profile", "validity"))

all_edges = []
for graph in bundle["graphs"].values():
    all_edges.extend(graph["edges"])
    for e in graph["edges"]:
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]]
        assert e["edge_id"] in graph["in"][e["to"]]
by_id = {e["edge_id"]: e for e in all_edges}
for e in bundle["graphs"]["proof"]["edges"]:
    reciprocal = by_id[e["reciprocal_edge_id"]]
    assert reciprocal["from"] == e["to"] and reciprocal["to"] == e["from"]
    assert {e["type"], reciprocal["type"]} == {"proof_requires", "composes"}

requires = [e for e in bundle["graphs"]["proof"]["edges"] if e["type"] == "proof_requires"]
children = {}
for e in requires:
    children.setdefault(e["from"], []).append(e["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M0989-ROOT")
assert {"M0989-S-MEAS", "M0989-T-CHARFUN"}.issubset(seen)
assert bundle["closure_boundary"]["root_closed"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert "root_of_row_charFun_packages" in lean and "ProbabilityMeasure.tendsto_iff_tendsto_charFun" in lean
assert not any(token in lean for token in ("sorry", "admit", "axiom"))
print(f"PASS THM-M-0989 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); row measurability and characteristic-function package remain open")
