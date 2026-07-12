#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-1141 obligation freeze."""
import hashlib, json
from pathlib import Path
H = Path(__file__).resolve().parent
r = json.loads((H / "obligation-registry.json").read_text())
g = json.loads((H / "typed-graphs.json").read_text())
s = json.loads((H / "validation-specs.json").read_text())
assert r["item_id"] == g["item_id"] == s["item_id"] == "S56-M-1141-OBLIGATION_TREE"
assert r["frozen_against_statement_sha256"] == hashlib.sha256((H / "Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"] == hashlib.sha256((H / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = r["obligations"]; ids = [x["obligation_id"] for x in rows]
assert len(ids) == len(set(ids)) == 11 and ids[0] == r["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k: x[k] for k in fields} for x in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == r["denominator_sha256"] == g["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"] == ids
assert {n["obligation_id"] for n in g["nodes"]} == set(ids)
assert all(0 < n["step_budget"] <= 100 for n in g["nodes"])
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in g["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]; seen.add(e["edge_id"])
proof = {e["edge_id"]: e for e in g["graphs"]["proof"]["edges"]}
for e in proof.values():
    q = proof[e["reciprocal_edge_id"]]
    assert q["reciprocal_edge_id"] == e["edge_id"] and (q["from"], q["to"]) == (e["to"], e["from"])
assert {n["validation_spec_id"] for n in g["nodes"]} == {x["recipe_id"] for x in s["recipes"]}
assert not g["closure_boundary"]["root_closed"] and not g["closure_boundary"]["theorem_complete"]
lean = (H / "ObligationTree.lean").read_text()
assert all(x not in lean for x in ("sorry", "admit", "axiom ", "sorryAx"))
assert "harnackInequality_of_uniformValueComparison" in lean and "#print axioms" in lean
print(f"PASS THM-M-1141 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print("registry denominator sha256:", digest)
print("root closure: open (M3); analytic and compact-chain packages remain M4")
