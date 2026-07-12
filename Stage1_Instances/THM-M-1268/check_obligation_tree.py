#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here=Path(__file__).resolve().parent
r=json.loads((here/"obligation-registry.json").read_text())
b=json.loads((here/"typed-graphs.json").read_text())
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
rows=r["obligations"]; ids=[x["obligation_id"] for x in rows]
raw=json.dumps([{k:x[k] for k in fields} for x in rows],sort_keys=True,separators=(",",":")).encode()
digest=hashlib.sha256(raw).hexdigest()
assert len(ids)==12==len(set(ids)) and ids[0]==r["root_obligation_id"]=="M1268-ROOT"
assert digest==r["denominator_sha256"]==b["registry_denominator_sha256"]
assert {n["obligation_id"] for n in b["nodes"]}==set(ids)
assert set(b["graphs"])=={"proof","refinement","provenance","evidence","trust","documentation","workflow"}
edges=set()
for name,g in b["graphs"].items():
  for e in g["edges"]:
    assert e["edge_id"] not in edges and e["from"] in ids and e["to"] in ids
    assert e["edge_id"] in g["out"][e["from"]] and e["edge_id"] in g["in"][e["to"]]
    edges.add(e["edge_id"])
for key,field,value in (("required_machine","machine_eligibility","required"),("required_human_source","human_source_eligibility","required"),("required_readable","readable_eligibility","required")):
  assert r["frozen_denominators"][key]==[x["obligation_id"] for x in rows if x[field]==value]
assert b["closure_boundary"]["closed_obligations"]==[] and not b["closure_boundary"]["theorem_complete"]
assert b["closure_boundary"]["remaining_root_cut_set"]==["M1268-L-CONVEX-SUBLEVEL","M1268-L-WEAK-CLOSURE","M1268-T-WEAK-TO-NORM"]
print(f"PASS THM-M-1268 obligation tree: {len(ids)} obligations, {len(edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); no proof or theorem completion claimed")
