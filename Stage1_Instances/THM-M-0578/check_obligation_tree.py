#!/usr/bin/env python3
"""Fail-closed structural checks for THM-M-0578 obligation artifacts."""
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
reg=json.loads((HERE/"obligation-registry.json").read_text()); graphs=json.loads((HERE/"typed-graphs.json").read_text()); specs=json.loads((HERE/"validation-specs.json").read_text())
assert reg["item_id"]==graphs["item_id"]==specs["item_id"]=="S56-M-0578-OBLIGATION_TREE"
obs=reg["obligations"]; ids=[o["obligation_id"] for o in obs]; assert len(ids)==len(set(ids))==13
assert reg["root_obligation_id"]==graphs["root_node_id"]=="M0578-ROOT"
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
raw=json.dumps([{k:o[k] for k in fields} for o in obs],sort_keys=True,separators=(",",":")).encode(); denom=hashlib.sha256(raw).hexdigest()
assert denom==reg["denominator_sha256"]==graphs["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"]==ids and {n["obligation_id"] for n in graphs["nodes"]}==set(ids)
needed={"semantic_step_ledger","step_budget","formal_target","validation_spec_id","validity","foundation_profile","tcb_profile","computation_record"}
assert all(needed<=n.keys() and 0<n["step_budget"]<=100 for n in graphs["nodes"])
all_edges=[]
for graph in graphs["graphs"].values():
 all_edges += graph["edges"]
 for e in graph["edges"]: assert e["from"] in ids and e["to"] in ids and e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
byid={e["edge_id"]:e for e in all_edges}; assert len(byid)==len(all_edges)
for e in graphs["graphs"]["proof"]["edges"]:
 r=byid[e["reciprocal_edge_id"]]; assert r["from"]==e["to"] and r["to"]==e["from"] and {e["type"],r["type"]}=={"proof_requires","composes"}
children={}
for e in graphs["graphs"]["proof"]["edges"]:
 if e["type"]=="proof_requires": children.setdefault(e["from"],[]).append(e["to"])
seen=set(); active=set()
def visit(n):
 assert n not in active
 if n in seen:return
 active.add(n)
 for c in children.get(n,[]):visit(c)
 active.remove(n);seen.add(n)
visit("M0578-ROOT")
assert set(graphs["closure_boundary"]["remaining_root_cut_set"])=={"M0578-C-BUNDLE","M0578-T-HOMEO","M0578-O-NONDIFF"}
assert not graphs["closure_boundary"]["root_closed"] and not graphs["closure_boundary"]["theorem_complete"]
assert {r["obligation_id"] for r in specs["recipes"]}==set(ids)
lean=(HERE/"ObligationTree.lean").read_text()
for bad in ("sorry","admit","axiom ","proof_wanted"):assert bad not in lean
assert "root_of_exoticWitnessPackage" in lean and "#print axioms" in lean
print(f"PASS THM-M-0578 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denom}")
print("root closure: open (M4); construction, homeomorphism, and nondiffeomorphism remain open")
