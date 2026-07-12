#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-1011 obligation freeze."""
from pathlib import Path
import hashlib, json, re

HERE=Path(__file__).resolve().parent
r=json.loads((HERE/"obligation-registry.json").read_text())
b=json.loads((HERE/"typed-graphs.json").read_text())
s=json.loads((HERE/"validation-specs.json").read_text())
assert r["item_id"]==b["item_id"]==s["item_id"]=="S56-M-1011-OBLIGATION_TREE"
assert r["theorem_id"]==b["theorem_id"]==s["theorem_id"]=="THM-M-1011"
assert r["frozen_against_statement_sha256"]==hashlib.sha256((HERE/"Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"]==hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest()
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
rows=r["obligations"]; ids=[x["obligation_id"] for x in rows]
assert len(ids)==len(set(ids))==14 and ids[0]==r["root_obligation_id"]=="M1011-ROOT"
payload=json.dumps([{k:x[k] for k in fields} for x in rows],sort_keys=True,separators=(",",":")).encode()
d=hashlib.sha256(payload).hexdigest()
assert d==r["denominator_sha256"]==b["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"]==ids
required={"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
assert len(b["nodes"])==len(ids) and {n["obligation_id"] for n in b["nodes"]}==set(ids)
for n in b["nodes"]:
 assert required<=n.keys() and 0<n["step_budget"]<=100
 assert {"premises","inference","output","outgoing_use"}<=n["semantic_step_ledger"].keys()
allowed={"proof_requires","composes","logical_decomposition","source_map","provenance_of","evidence_for","trusts","documents","workflow_depends_on"}
assert set(b["graphs"])=={"proof","refinement","provenance","evidence","trust","documentation","workflow"}
seen=set()
for graph in b["graphs"].values():
 for e in graph["edges"]:
  assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids
  assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]; seen.add(e["edge_id"])
proof={e["edge_id"]:e for e in b["graphs"]["proof"]["edges"]}; children={}
for e in proof.values():
 q=proof[e["reciprocal_edge_id"]]
 assert q["reciprocal_edge_id"]==e["edge_id"] and (q["from"],q["to"])==(e["to"],e["from"])
 assert {e["type"],q["type"]}=={"proof_requires","composes"}
 if e["type"]=="proof_requires": children.setdefault(e["from"],[]).append(e["to"])
visiting=set(); visited=set()
def visit(x):
 assert x not in visiting
 if x in visited:return
 visiting.add(x)
 for y in children.get(x,[]):visit(y)
 visiting.remove(x);visited.add(x)
visit("M1011-ROOT")
assert visited=={"M1011-ROOT","M1011-T-ASSEMBLE","M1011-B-TIGHT-COMPACT","M1011-B-COMPACT-TIGHT","M1011-N-SEPARATION","M1011-L-PROKHOROV","M1011-L-COMPACT-TIGHT"}
assert {n["validation_spec_id"] for n in b["nodes"]}=={x["recipe_id"] for x in s["recipes"]}
for x in s["recipes"]:
 assert x["argv"]==["python3","Stage1_Instances/THM-M-1011/check_obligation_tree.py"] and x["network_policy"]=="denied" and x["expected_exit"]==0
assert not b["closure_boundary"]["root_closed"] and not b["closure_boundary"]["theorem_complete"]
lean=(HERE/"ObligationTree.lean").read_text()
assert re.search(r"\b(sorry|admit|axiom|sorryAx)\b",lean,re.I) is None
assert "canonical_of_t2" in lean and "#print axioms canonical_of_t2" in lean
print(f"PASS THM-M-1011 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {d}")
print("root closure: open (M5); exact frozen context does not supply T2Space X")
