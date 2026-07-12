#!/usr/bin/env python3
"""Build the frozen THM-M-1011 obligation registry and typed graphs."""

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1011-OBLIGATION_TREE"
THEOREM = "THM-M-1011"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def planned(text): return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

data = [
 ("M1011-ROOT", "root", "The exact frozen Prokhorov equivalence for every family of probability measures.", "Stage1Instances.THM_M_1011.CanonicalStatement", "The exact canonical equivalence.", "critical", "M5", "H1", "required", "required", "required"),
 ("M1011-S-DEFINITIONS", "definition", "Freeze ProbabilityMeasure, underlyingMeasures, uniform tightness, weak topology, closure, and compactness.", "Stage1Instances.THM_M_1011.{underlyingMeasures,IsUniformlyTight}", "The exact vocabulary of the root.", "high", "M0-L", "H3", "required", "not_applicable", "required"),
 ("M1011-S-DOMAIN", "normalization", "Preserve the ordered Polish-space binders and expose that PseudoMetricSpace does not synthesize T2Space.", "checked binder context plus failed T2Space synthesis in AnchorAudit.lean", "The exact typeclass boundary.", "critical", "M0-W", "H3", "required", "not_applicable", "required"),
 ("M1011-S-BOUNDARY", "terminal", "Cover empty, singleton, finite, and arbitrary measure families without a nonempty-family assumption.", "planned exact boundary lemmas for CanonicalStatement", "The degenerate-family boundary.", "normal", "M4", "H3", "required", "not_applicable", "required"),
 ("M1011-S-TRANSPORT", "transport", "Relate the local tightness alias to IsTightMeasureSet and relative compactness to compact closure only in checked directions.", "Stage1Instances.THM_M_1011.canonicalStatement_iff", "Checked representation transport.", "high", "M0-L", "H2", "required", "required", "required"),
 ("M1011-S-FOUNDATION", "certificate", "Audit classical choice, quotients, extensionality, the Lean kernel, mathlib, and the no-oracle boundary.", "planned transitive trust and axiom report", "The foundation and TCB policy.", "high", "M3", "H3", "required", "not_applicable", "required"),
 ("M1011-N-SEPARATION", "reduction", "Resolve whether the frozen pseudo-metric hypotheses supply the T2 separation needed by the forward mathlib anchor, without strengthening the target.", "planned exact bridge: frozen context -> T2Space X, or a statement correction", "A legal separation input for the forward direction.", "critical", "M5", "H1", "required", "required", "required"),
 ("M1011-B-TIGHT-COMPACT", "branch", "From uniform tightness, prove compactness of the weak closure for the exact frozen context.", "Stage1Instances.THM_M_1011.ObligationTree.tight_to_compact_of_t2 (conditional)", "The forward implication.", "critical", "M5", "H1", "required", "required", "required"),
 ("M1011-B-COMPACT-TIGHT", "branch", "From compactness of the weak closure, prove uniform tightness for the exact frozen context.", "Stage1Instances.THM_M_1011.ObligationTree.compact_to_tight", "The reverse implication.", "high", "M0-W", "H1", "required", "required", "required"),
 ("M1011-L-PROKHOROV", "bridge", "Apply pinned mathlib's tight-measure-set compactness theorem with every required instance explicit.", "MeasureTheory.isCompact_closure_of_isTightMeasureSet", "Tightness implies compact closure under T2Space.", "critical", "M5", "H1", "required", "required", "required"),
 ("M1011-L-COMPACT-TIGHT", "bridge", "Apply pinned mathlib's compact-closure tightness theorem after exact coercion normalization.", "MeasureTheory.isTightMeasureSet_of_isCompact_closure", "Compact closure implies tightness.", "high", "M0-W", "H1", "required", "required", "required"),
 ("M1011-T-ASSEMBLE", "terminal", "Merge both implications into the exact iff while consuming the explicit separation child.", "Stage1Instances.THM_M_1011.ObligationTree.canonical_of_t2", "The conditional canonical root.", "critical", "M5", "H1", "required", "required", "required"),
 ("M1011-X-SOURCE", "terminal", "Crosswalk every material node to a pinpoint primary-source theorem, assumptions, conventions, and errata.", "not-applicable to Lean; structured H review pending", "Human-source provenance coverage.", "high", "M3", "H1", "not_applicable", "required", "required"),
 ("M1011-X-PROVENANCE", "terminal", "Record terminal bodies, wrappers, dependency revision, axioms, placeholders, and license boundary without duplicating proof credit.", "anchor-audit.json and planned transitive declaration closure", "Machine provenance overlay.", "high", "M3", "H3", "informational", "not_applicable", "required"),
]

obligations=[]
for oid,kind,human,formal,output,risk,machine,hdebt,melig,helig,relig in data:
    fp = "lean-expression-sha256:5711575e18ff4a1eecd2ce047a29817d876a6e44cb86c724b476414314f9e812" if oid == "M1011-ROOT" else planned(formal)
    obligations.append({"obligation_id":oid,"statement_fingerprint":fp,"kind":kind,"root_relevant":True,
      "machine_eligibility":melig,"human_source_eligibility":helig,"readable_eligibility":relig,
      "risk_class":risk,"exclusion_reason":None,"terminal_proof_body_id":
      ("mathlib:isTightMeasureSet_of_isCompact_closure@8a178386" if oid in {"M1011-B-COMPACT-TIGHT","M1011-L-COMPACT-TIGHT"} else None)})
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
payload=json.dumps([{k:o[k] for k in fields} for o in obligations],sort_keys=True,separators=(",",":")).encode()
denom=hashlib.sha256(payload).hexdigest()
ids=[o["obligation_id"] for o in obligations]
registry={"schema_version":"stage1-obligation-registry/1.0","item_id":ITEM,"theorem_id":THEOREM,
 "registry_version":1,"frozen_at":"2026-07-12T00:00:00+08:00",
 "freeze_basis":"Exact statement and bounded anchor audit, frozen before obligation closure metrics; eligibility follows semantic role, including the discovered separation mismatch.",
 "frozen_against_statement_sha256":sha(HERE/"Statement.lean"),"frozen_against_anchor_audit_sha256":sha(HERE/"anchor-audit.json"),
 "root_obligation_id":"M1011-ROOT","denominator_sha256":denom,
 "frozen_denominators":{"inventory":ids,"required_machine":[o["obligation_id"] for o in obligations if o["machine_eligibility"]=="required"],
  "required_human_source":[o["obligation_id"] for o in obligations if o["human_source_eligibility"]=="required"],
  "required_readable":[o["obligation_id"] for o in obligations if o["readable_eligibility"]=="required"],"informational_overlays":["M1011-X-PROVENANCE"]},
 "delta_policy":"Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.","obligations":obligations}

nodes=[]
for oid,kind,human,formal,output,risk,machine,hdebt,*_ in data:
 nodes.append({"node_id":f"THM-M-1011-{oid[6:]}","obligation_id":oid,"kind":kind,"human_statement":human,"formal_target":formal,"output":output,
  "human_debt":hdebt,"machine_debt":machine,"readability_debt":"R3" if oid.startswith("M1011-X") else "R4","evidence_ids":[],
  "source_crosswalk_id":"prohorov-primary-crosswalk-pending" if hdebt in {"H1","H2"} else "not-applicable","provenance_id":"M1011-AUDIT" if oid.startswith("M1011-L") else "none",
  "foundation_profile":"Lean 4 dependent type theory; classical/quotient audit pending","tcb_profile":"Lean 4.29.0 + mathlib 8a178386; transitive closure pending",
  "computation_record":"none; no computation, oracle, or native result closes this node","step_budget":100,
  "semantic_step_ledger":{"premises":"Exact typed proof children and the frozen context only.","inference":human,"output":output,"outgoing_use":"Only declared typed edges may consume this output."},
  "public_readable_target":f"Stage1_Instances/THM-M-1011/obligation-tree.md#{oid.lower()}","validation_spec_id":f"VAL-{oid}",
  "status_boundary":"Architecture or conditional interface only; no missing premise or open child is discharged.","task_ids":[ITEM,"S56-M-1011-PROOF"],
  "owned_sources":["Stage1_Instances/THM-M-1011/ObligationTree.lean"] if oid in {"M1011-B-TIGHT-COMPACT","M1011-B-COMPACT-TIGHT","M1011-T-ASSEMBLE"} else [],
  "owner":"THM-M-1011 proof lane","reviewer":"independent Stage1 integration lane","validity":{"validated_at":"2026-07-12" if machine in {"M0-L","M0-W"} else None,"review_due":"before proof acceptance","invalidation_inputs":["statement","registry","anchor audit","toolchain"],"revocation_state":"provisional" if machine in {"M0-L","M0-W"} else "open"}})

graphs={name:{"edges":[],"out":{i:[] for i in ids},"in":{i:[] for i in ids}} for name in ("proof","refinement","provenance","evidence","trust","documentation","workflow")}
def edge(graph,typ,a,b,reciprocal=None):
 eid=f"{graph.upper()}-{len(graphs[graph]['edges'])+1:03d}"
 e={"edge_id":eid,"type":typ,"from":a,"to":b}
 if reciprocal: e["reciprocal_edge_id"]=reciprocal
 graphs[graph]["edges"].append(e); graphs[graph]["out"][a].append(eid); graphs[graph]["in"][b].append(eid); return eid
def proof_pair(parent,child):
 a=f"PROOF-{len(graphs['proof']['edges'])+1:03d}"; b=f"PROOF-{len(graphs['proof']['edges'])+2:03d}"
 edge("proof","proof_requires",parent,child,b); edge("proof","composes",child,parent,a)
for p,c in [("M1011-ROOT","M1011-T-ASSEMBLE"),("M1011-T-ASSEMBLE","M1011-B-TIGHT-COMPACT"),("M1011-T-ASSEMBLE","M1011-B-COMPACT-TIGHT"),("M1011-B-TIGHT-COMPACT","M1011-N-SEPARATION"),("M1011-B-TIGHT-COMPACT","M1011-L-PROKHOROV"),("M1011-B-COMPACT-TIGHT","M1011-L-COMPACT-TIGHT")]: proof_pair(p,c)
for child in ("M1011-S-DEFINITIONS","M1011-S-DOMAIN","M1011-S-BOUNDARY","M1011-S-TRANSPORT","M1011-S-FOUNDATION"):
 edge("refinement","logical_decomposition","M1011-ROOT",child)
for child in ("M1011-X-SOURCE","M1011-X-PROVENANCE"):
 edge("provenance","source_map" if child.endswith("SOURCE") else "provenance_of",child,"M1011-ROOT")
for oid in ids: edge("documentation","documents",oid,"M1011-ROOT") if oid != "M1011-ROOT" else None
edge("trust","trusts","M1011-ROOT","M1011-S-FOUNDATION")
edge("evidence","evidence_for","M1011-X-PROVENANCE","M1011-L-PROKHOROV")
edge("workflow","workflow_depends_on","M1011-T-ASSEMBLE","M1011-N-SEPARATION")
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":ITEM,"theorem_id":THEOREM,"registry_id":"THM-M-1011-OBLIGATIONS-v1","registry_denominator_sha256":denom,
 "root_node_id":"M1011-ROOT","edge_direction":"proof_requires runs parent to child; reciprocal composes runs child to parent.","nodes":nodes,"graphs":graphs,
 "closure_boundary":{"root_closed":False,"root_machine_debt":"M5","theorem_complete":False,"first_failed_gate":"exact statement match / missing T2Space X","remaining_root_cut_set":["M1011-N-SEPARATION"],"conditional_composition":"Stage1Instances.THM_M_1011.ObligationTree.canonical_of_t2"}}
recipes=[]
for oid in ids:
 recipes.append({"recipe_id":f"VAL-{oid}","cwd":".","argv":["python3","Stage1_Instances/THM-M-1011/check_obligation_tree.py"],"env_allowlist":{},"timeout_seconds":30,"network_policy":"denied","expected_exit":0,
  "expected_outputs":[{"path_or_stream":"stdout","semantic_hash_policy":"contains PASS THM-M-1011 obligation tree"}],"covered_obligation_ids":[oid],"covered_declarations":[]})
specs={"schema_version":"stage1-validation-specs/1.0","item_id":ITEM,"theorem_id":THEOREM,"recipes":recipes}
for name,obj in (("obligation-registry.json",registry),("typed-graphs.json",bundle),("validation-specs.json",specs)):
 (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=True)+"\n")
print(denom)
