#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-1247 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1247-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1247"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 13 and ids[0] == registry["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
required = {"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
nodes = bundle["nodes"]
assert len(nodes) == 13 and {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises","inference","output","outgoing_use"} <= n["semantic_step_ledger"].keys()
allowed = {"proof_requires","composes","source_map","provenance_of","trusts","documents","workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        seen.add(e["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}; children = {}
for e in proof.values():
    rev = proof[e["reciprocal_edge_id"]]
    assert rev["reciprocal_edge_id"] == e["edge_id"] and (rev["from"],rev["to"]) == (e["to"],e["from"])
    assert {e["type"],rev["type"]} == {"proof_requires","composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting=set(); visited=set()
def visit(x):
    assert x not in visiting
    if x in visited: return
    visiting.add(x)
    for y in children.get(x,[]): visit(y)
    visiting.remove(x); visited.add(x)
visit("M1247-ROOT")
assert visited == {"M1247-ROOT","M1247-T-TRANSPORT","M1247-L-CORE","M1247-L-IBP","M1247-L-HARDY","M1247-N-WEIGHTS","M1247-S-BOUNDARY","M1247-S-DOMAIN","M1247-S-LAPLACIAN"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_coreRellichEstimate" in lean and "#print axioms" in lean
print(f"PASS THM-M-1247 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); six analytic obligations remain M4")
