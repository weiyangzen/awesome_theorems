#!/usr/bin/env python3
"""Fail-closed structural validator for the THM-M-0464 obligation freeze."""
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
def require(v, msg):
    if not v: raise SystemExit("obligation-tree check failed: " + msg)

require(registry["item_id"] == bundle["item_id"] == "S56-M-0464-OBLIGATION_TREE", "wrong item")
require(registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0464", "wrong theorem")
require(registry["depends_on"] == ["S56-M-0464-ANCHOR_AUDIT"], "wrong prerequisite")
require(registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE/"Statement.lean").read_bytes()).hexdigest(), "statement drift")
require(registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest(), "anchor drift")
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
rows=registry["obligations"]; ids=[r["obligation_id"] for r in rows]
require(len(ids)==len(set(ids))==16, "expected 16 unique obligations")
digest=hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows],sort_keys=True,separators=(",",":")).encode()).hexdigest()
require(digest==registry["denominator_sha256"]==bundle["registry_denominator_sha256"], "denominator drift")
for key, predicate in (("inventory",lambda r:True),("required_machine",lambda r:r["machine_eligibility"]=="required"),("required_human_source",lambda r:r["human_source_eligibility"]=="required"),("required_readable",lambda r:r["readable_eligibility"]=="required")):
    require(registry["frozen_denominators"][key]==[r["obligation_id"] for r in rows if predicate(r)], key+" mismatch")
required_node_fields={"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
require(len(bundle["nodes"])==16 and {n["obligation_id"] for n in bundle["nodes"]}==set(ids), "node coverage")
require(all(required_node_fields <= set(n) and 0<n["step_budget"]<=100 for n in bundle["nodes"]), "node schema/budget")
require(set(bundle["graphs"])=={"proof","refinement","provenance","evidence","trust","documentation","workflow"}, "graph families")
allowed={"proof_requires","refines","provenance_of","evidence_for","trusts","documents","workflow_depends_on"}; edge_ids=set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        require(e["type"] in allowed and e["from"] in ids and e["to"] in ids, "illegal edge")
        require(e["edge_id"] not in edge_ids and e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]], "edge reciprocity")
        edge_ids.add(e["edge_id"])
children={}
for e in bundle["graphs"]["proof"]["edges"]: children.setdefault(e["from"],[]).append(e["to"])
visiting=set(); visited=set()
def visit(x):
    require(x not in visiting,"proof cycle")
    if x in visited:return
    visiting.add(x)
    for y in children.get(x,[]):visit(y)
    visiting.remove(x);visited.add(x)
visit("M0464-ROOT")
require(set(registry["closure_boundary"]["immediate_root_cut_set"]) <= visited, "cut set unreachable")
lean=(HERE/"ObligationTree.lean").read_text()
require(not any(t in lean for t in ("sorry","admit","axiom ","sorryAx")), "prohibited Lean token")
require("root_from_terminal_counting" in lean and "#print axioms" in lean, "composition probe absent")
require(bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False,"false closure")
print(f"PASS THM-M-0464 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print("registry denominator sha256:", digest)
print("root closure: open (M3); all Pila-Wilkie mathematical packages remain open")
