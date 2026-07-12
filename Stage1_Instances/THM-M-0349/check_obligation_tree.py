#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0349 obligation freeze."""
import hashlib, json
from pathlib import Path
H=Path(__file__).resolve().parent
r=json.loads((H/"obligation-registry.json").read_text()); b=json.loads((H/"typed-graphs.json").read_text())
assert r["item_id"]==b["item_id"]=="S56-M-0349-OBLIGATION_TREE" and r["theorem_id"]==b["theorem_id"]=="THM-M-0349"
assert r["frozen_against_statement_sha256"]==hashlib.sha256((H/"Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"]==hashlib.sha256((H/"anchor-audit.json").read_bytes()).hexdigest()
rows=r["obligations"]; ids=[x["obligation_id"] for x in rows]; fields=tuple(rows[0])
assert len(ids)==len(set(ids))==15 and ids[0]==r["root_obligation_id"]
d=hashlib.sha256(json.dumps([{k:x[k] for k in fields} for x in rows],sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert d==r["denominator_sha256"]==b["registry_denominator_sha256"] and r["frozen_denominators"]["inventory"]==ids
nodes=b["nodes"]; assert len(nodes)==15 and {n["obligation_id"] for n in nodes}==set(ids)
for n in nodes:
 assert 0<n["step_budget"]<=100 and {"premises","inference","output","outgoing_use"}<=n["semantic_step_ledger"].keys()
allowed={"proof_requires","composes","logical_decomposition","source_map","provenance_of","trusts","workflow_depends_on"}; seen=set()
for g in b["graphs"].values():
 for e in g["edges"]:
  assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids
  assert e["edge_id"] in g["out"][e["from"]] and e["edge_id"] in g["in"][e["to"]]; seen.add(e["edge_id"])
pe={e["edge_id"]:e for e in b["graphs"]["proof"]["edges"]}; children={}
for e in pe.values():
 q=pe[e["reciprocal_edge_id"]]; assert q["reciprocal_edge_id"]==e["edge_id"] and (q["from"],q["to"])==(e["to"],e["from"])
 if e["type"]=="proof_requires": children.setdefault(e["from"],[]).append(e["to"])
visiting=set(); visited=set()
def visit(x):
 assert x not in visiting
 if x in visited:return
 visiting.add(x)
 for y in children.get(x,[]):visit(y)
 visiting.remove(x);visited.add(x)
visit("M0349-ROOT")
assert visited=={"M0349-ROOT","M0349-T-ASSEMBLE","M0349-P-EXISTENCE","M0349-P-BOUND","M0349-D-DENSE","M0349-C-POLYNOMIAL","M0349-L-WEAK11","M0349-L-L2","M0349-L-INTERPOLATE","M0349-C-EXTEND","M0349-L-FOURIER-ID"}
assert b["closure_boundary"]=={"root_closed":False,"theorem_complete":False,"minimal_open_root_cut":["M0349-P-EXISTENCE","M0349-P-BOUND"]}
lean=(H/"ObligationTree.lean").read_text(); assert all(x not in lean for x in ("sorry","admit","axiom ","sorryAx")); assert "root_of_conjugate_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-0349 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {d}")
print("root closure: open (M3); existence and uniform-bound packages remain M4")
