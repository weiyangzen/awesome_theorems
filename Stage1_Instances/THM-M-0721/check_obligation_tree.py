#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0721 obligation freeze."""
import hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
reg=json.loads((HERE/"obligation-registry.json").read_text()); bun=json.loads((HERE/"typed-graphs.json").read_text()); specs=json.loads((HERE/"validation-specs.json").read_text())
assert reg["item_id"]==bun["item_id"]==specs["item_id"]=="S56-M-0721-OBLIGATION_TREE"
assert reg["frozen_against_statement_sha256"]==hashlib.sha256((HERE/"Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"]==hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest()
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
rows=reg["obligations"]; ids=[r["obligation_id"] for r in rows]
assert len(ids)==len(set(ids))==18 and ids[0]==reg["root_obligation_id"]=="M0721-ROOT"
projection=[{k:r[k] for k in fields} for r in rows]
digest=hashlib.sha256(json.dumps(projection,sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert digest==reg["denominator_sha256"]==bun["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"]==ids
required={"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
assert {n["obligation_id"] for n in bun["nodes"]}==set(ids)
for n in bun["nodes"]:
 assert required<=n.keys() and 0<n["step_budget"]<=100
 assert {"premises","inference","output","outgoing_use"}<=n["semantic_step_ledger"].keys()
allowed={"proof_requires","composes","logical_decomposition","source_map","provenance_of","trusts","documents","workflow_depends_on"}; edge_ids=set()
for graph in bun["graphs"].values():
 for e in graph["edges"]:
  assert e["edge_id"] not in edge_ids and e["type"] in allowed and e["from"] in ids and e["to"] in ids
  assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]; edge_ids.add(e["edge_id"])
proof={e["edge_id"]:e for e in bun["graphs"]["proof"]["edges"]}; children={}
for e in proof.values():
 reverse=proof[e["reciprocal_edge_id"]]; assert reverse["reciprocal_edge_id"]==e["edge_id"] and (reverse["from"],reverse["to"])==(e["to"],e["from"])
 assert {e["type"],reverse["type"]}=={"proof_requires","composes"}
 if e["type"]=="proof_requires": children.setdefault(e["from"],[]).append(e["to"])
visiting=set(); visited=set()
def visit(x):
 assert x not in visiting
 if x in visited:return
 visiting.add(x)
 for y in children.get(x,[]):visit(y)
 visiting.remove(x);visited.add(x)
visit("M0721-ROOT")
assert set(bun["closure_boundary"]["remaining_root_cut_set"])=={"M0721-T-SAT-IN-NP","M0721-T-UNIVERSAL-HARDNESS"}
assert bun["closure_boundary"]["root_closed"] is False and bun["closure_boundary"]["theorem_complete"] is False
assert {n["validation_spec_id"] for n in bun["nodes"]}=={r["recipe_id"] for r in specs["recipes"]}
lean=(HERE/"ObligationTree.lean").read_text(); assert all(t not in lean for t in ("sorry","admit","axiom ","sorryAx"))
assert "root_of_candidate_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-0721 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); SAT membership and universal Cook-Levin hardness remain M4")
