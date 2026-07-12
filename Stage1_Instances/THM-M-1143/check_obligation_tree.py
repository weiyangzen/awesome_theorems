#!/usr/bin/env python3
"""Fail-closed structural check for the THM-M-1143 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())
obligations = registry["obligations"]
ids = [o["obligation_id"] for o in obligations]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] in ids
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
payload = [{k: o[k] for k in fields} for o in obligations]
digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert set(ids) == {n["obligation_id"] for n in bundle["nodes"]}
assert set(ids) == {r["obligation_id"] for r in recipes["recipes"]}
all_edges = [e for graph in bundle["graphs"].values() for e in graph["edges"]]
edge_ids = {e["edge_id"] for e in all_edges}
assert len(edge_ids) == len(all_edges)
assert all(e["from"] in ids and e["to"] in ids for e in all_edges)
proof = bundle["graphs"]["proof"]
for e in proof["edges"]:
    if e["type"] == "proof_requires":
        reciprocal = next(x for x in proof["edges"] if x["edge_id"] == e["reciprocal_edge_id"])
        assert reciprocal["type"] == "composes" and reciprocal["from"] == e["to"] and reciprocal["to"] == e["from"]
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] in graph["out"][e["from"]]
        assert e["edge_id"] in graph["in"][e["to"]]
assert not bundle["closure_boundary"]["root_closed"]
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1143-T-VANISH", "M1143-L-CONSTANT"]
lean = (HERE / "ObligationTree.lean").read_text()
assert "root_of_vanishingDerivative_packages" in lean and "#print axioms" in lean
assert all(word not in lean for word in ("sorry", "admit", "axiom "))
print(f"PASS THM-M-1143 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); derivative-vanishing and constancy packages remain explicit")
