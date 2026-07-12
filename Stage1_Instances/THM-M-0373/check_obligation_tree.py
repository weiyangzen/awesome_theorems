#!/usr/bin/env python3
"""Validate the THM-M-0373 frozen obligation architecture."""
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
load=lambda n: json.loads((HERE/n).read_text())
r=load("obligation-registry.json"); b=load("typed-graphs.json")
assert r["item_id"]==b["item_id"]=="S56-M-0373-OBLIGATION_TREE"
assert r["frozen_against_statement_sha256"]==hashlib.sha256((HERE/"statement.json").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"]==hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest()
rows=r["obligations"]; ids=[x["obligation_id"] for x in rows]; assert len(ids)==len(set(ids))==20
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
digest=hashlib.sha256(json.dumps([{k:x[k] for k in fields} for x in rows],sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert digest==r["denominator_sha256"]==b["registry_denominator_sha256"]
assert {n["obligation_id"] for n in b["nodes"]}==set(ids)
assert all(0<n["step_budget"]<=100 and set(n["semantic_step_ledger"])=={"premises","inference","output","outgoing_use"} for n in b["nodes"])
allowed={"proof_requires","composes","logical_decomposition","provenance_of","evidence_for","trusts","documents","workflow_depends_on"}; seen=set()
children={}
for g in b["graphs"].values():
  for e in g["edges"]:
    assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids; seen.add(e["edge_id"])
    assert e["edge_id"] in g["out"][e["from"]] and e["edge_id"] in g["in"][e["to"]]
for e in b["graphs"]["proof"]["edges"]:
  if e["type"]=="proof_requires": children.setdefault(e["from"],[]).append(e["to"])
active=set(); visited=set()
def visit(x):
  assert x not in active
  if x in visited:return
  active.add(x)
  for y in children.get(x,[]):visit(y)
  active.remove(x);visited.add(x)
visit("M0373-ROOT")
assert set(r["frozen_denominators"]["required_machine"])<=visited
assert b["closure_boundary"]["closed_obligations"]==[] and not b["closure_boundary"]["root_closed"]
lean=(HERE/"ObligationTree.lean").read_text(); assert all(x not in lean for x in ("sorry","admit","axiom ","sorryAx")); assert "root_compose" in lean
print(f"PASS THM-M-0373 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains M4 and uncredited; analytic and dbar construction cut remains open")
