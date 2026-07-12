#!/usr/bin/env python3
"""Build the frozen THM-M-0578 obligation registry and typed graphs."""
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM = "S56-M-0578-OBLIGATION_TREE", "THM-M-0578"
def sha(x): return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

rows = [
 ("M0578-ROOT","root","critical","Existence of a smooth seven-manifold homeomorphic but not diffeomorphic to the standard smooth seven-sphere.","Stage1Instances.THM_M_0578.MilnorExoticSphereTarget","Canonical proposition"),
 ("M0578-S-MODELS","definition","high","Freeze unit S^7, seven-dimensional charts, smoothness infinity, and the unoriented diffeomorphism boundary.","Stage1Instances.THM_M_0578.{MilnorExoticSphereTarget,PinnedCandidateSourceShape}","Exact elaborated models"),
 ("M0578-C-BUNDLE","construction","critical","Construct a specified Milnor S^3-bundle over S^4 and its smooth seven-dimensional total space M.","planned Lean Milnor bundle construction","Smooth candidate M"),
 ("M0578-C-BOUNDARY","certificate","high","Check bundle parameter, orientation reversal, dimension, compactness, and sphere conventions.","planned construction boundary certificate","Construction conventions"),
 ("M0578-T-HOMOTOPY","lemma","critical","Compute the candidate's homotopy type and establish homotopy-seven-sphere hypotheses.","planned homotopy-sphere certificate","Homotopy-sphere data"),
 ("M0578-T-HOMEO","bridge","critical","Deduce an exact homeomorphism M ≃ₜ S^7 by a proof-bearing topological classification route.","planned exact homeomorphism theorem","Homeomorphism to fixed unit S^7"),
 ("M0578-I-CANDIDATE","computation","critical","Compute a normalized diffeomorphism invariant of the candidate, including orientation behavior.","planned Eells-Kuiper or equivalent invariant computation","Candidate invariant value"),
 ("M0578-I-STANDARD","computation","critical","Compute the same normalized invariant for the standard smooth seven-sphere.","planned standard-sphere invariant computation","Standard invariant value"),
 ("M0578-O-NONDIFF","lemma","critical","Use invariant preservation and unequal values to prove the diffeomorphism type empty.","planned IsEmpty Diffeomorph obstruction","No diffeomorphism M ≃ₘ S^7"),
 ("M0578-T-PACKAGE","transport","high","Package the constructed manifold, homeomorphism, and obstruction and transport to the exact root.","Stage1Instances.THM_M_0578.ObligationTree.root_of_exoticWitnessPackage","Canonical proposition conditionally"),
 ("M0578-X-SOURCE","source","high","Crosswalk every material step to reviewed primary-source theorem/page/assumption/errata passages.","non-machine node source crosswalk","Human-source coverage only"),
 ("M0578-X-FOUNDATION","certificate","critical","Record choice, quotients, topology, manifolds, invariant machinery, TCB, and no-oracle boundaries.","planned transitive axiom and TCB report","Foundation boundary"),
 ("M0578-X-PROVENANCE","certificate","critical","Inventory terminal bodies, wrappers, imports, revisions, licenses, and replay receipts.","planned provenance closure","Release overlay"),
]
checked={"M0578-S-MODELS","M0578-T-PACKAGE"}; source_na={"M0578-S-MODELS","M0578-X-FOUNDATION","M0578-X-PROVENANCE"}
special={"M0578-X-SOURCE":"not_applicable","M0578-X-PROVENANCE":"informational"}
rootfp="lean-expression-sha256:c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c"
obs=[]; nodes=[]
for oid,kind,risk,claim,target,output in rows:
 machine=special.get(oid,"required")
 obs.append({"obligation_id":oid,"statement_fingerprint":rootfp if oid in {"M0578-ROOT","M0578-S-MODELS"} else "planned:v1:sha256:"+sha([oid,claim,target,output]),"kind":kind,"root_relevant":True,"machine_eligibility":machine,"human_source_eligibility":"not_applicable" if oid in source_na else "required","readable_eligibility":"required","risk_class":risk,"exclusion_reason":"human_source_boundary_only" if machine=="not_applicable" else ("release_overlay_no_proof_credit" if machine=="informational" else None),"terminal_proof_body_id":"local:Stage1_Instances/THM-M-0578/ObligationTree.lean#root_of_exoticWitnessPackage" if oid=="M0578-T-PACKAGE" else None})
 nodes.append({"node_id":"THM-M-0578-"+oid.removeprefix("M0578-"),"obligation_id":oid,"kind":kind,"human_statement":claim,"formal_target":target,"output":output,"human_debt":"H3","machine_debt":"M0-L" if oid in checked else "M4","readability_debt":"R4","evidence_ids":[],"source_crosswalk_id":"not-applicable" if oid in source_na else "primary-source-node-map-pending","provenance_id":"local-conditional-composition" if oid=="M0578-T-PACKAGE" else "none","foundation_profile":"lean4-mathlib-classical/policy-audit-pending","tcb_profile":"lean-4.29.0+mathlib-8a178386/transitive-closure-pending","computation_record":"No external computation is credited; invariant results require kernel-checked certificates.","step_budget":100 if oid in {"M0578-C-BUNDLE","M0578-T-HOMEO","M0578-I-CANDIDATE"} else 40,"semantic_step_ledger":{"premises":"Only declared proof_requires children and the formal context.","inference":claim,"output":output,"outgoing_use":"Only declared typed edges may consume this output."},"public_readable_target":"Stage1_Instances/THM-M-0578/obligation-tree.md#"+oid.lower(),"validation_spec_id":"VAL-"+oid,"status_boundary":"Frozen architecture or conditional interface only; no root closure.","task_ids":[ITEM,"S56-M-0578-PROOF"],"owned_sources":["Stage1_Instances/THM-M-0578/ObligationTree.lean"] if oid=="M0578-T-PACKAGE" else [],"owner":"THM-M-0578 proof lane","reviewer":"independent Stage1 integration lane","validity":{"validated_at":"2026-07-12" if oid in checked else None,"review_due":"before proof acceptance","invalidation_inputs":["statement","registry","source map","toolchain"],"revocation_state":"provisional" if oid in checked else "open"}})
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
denom=sha([{k:o[k] for k in fields} for o in obs]); ids=[r[0] for r in rows]
registry={"schema_version":"stage1-obligation-registry/1.0","item_id":ITEM,"theorem_id":THEOREM,"registry_version":1,"frozen_at":"2026-07-12T00:00:00+08:00","freeze_basis":"Exact statement and immutable anchor audit; Milnor bundle/topological classification/invariant obstruction architecture selected before closure metrics.","frozen_against_statement_sha256":hashlib.sha256((HERE/"Statement.lean").read_bytes()).hexdigest(),"frozen_against_anchor_audit_sha256":hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest(),"root_obligation_id":"M0578-ROOT","denominator_sha256":denom,"frozen_denominators":{"inventory":ids,"required_machine":[o["obligation_id"] for o in obs if o["machine_eligibility"]=="required"],"required_human_source":[o["obligation_id"] for o in obs if o["human_source_eligibility"]=="required"],"required_readable":ids,"informational_overlays":["M0578-X-PROVENANCE"]},"delta_policy":"Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only delta.","obligations":obs,"append_only_delta":[],"status_observed_after_freeze":{"closed_obligations":sorted(checked),"root_machine_debt":"M4"},"status_boundary":"Scope and denominators only; no construction, classification proof, invariant obstruction, or theorem completion."}
def edge(eid,a,t,b,rec=None):
 d={"edge_id":eid,"from":a,"type":t,"to":b}
 if rec:d["reciprocal_edge_id"]=rec
 return d
requires={"M0578-ROOT":["M0578-T-PACKAGE"],"M0578-T-PACKAGE":["M0578-C-BUNDLE","M0578-T-HOMEO","M0578-O-NONDIFF"],"M0578-C-BUNDLE":["M0578-C-BOUNDARY"],"M0578-T-HOMEO":["M0578-T-HOMOTOPY"],"M0578-O-NONDIFF":["M0578-I-CANDIDATE","M0578-I-STANDARD"]}
proof=[]
for parent,children in requires.items():
 for child in children:
  req,comp="REQ-"+parent+"-"+child,"CMP-"+child+"-"+parent; proof += [edge(req,parent,"proof_requires",child,comp),edge(comp,child,"composes",parent,req)]
edge_sets={"proof":proof,"refinement":[edge("REF-ROOT-MODELS","M0578-ROOT","logical_decomposition","M0578-S-MODELS"),edge("REF-CONSTR-BOUND","M0578-C-BUNDLE","boundary_refinement","M0578-C-BOUNDARY")],"provenance":[edge("SRC-ROUTE","M0578-X-SOURCE","source_of","M0578-T-PACKAGE"),edge("PROV-ROOT","M0578-X-PROVENANCE","provenance_of","M0578-ROOT")],"evidence":[],"trust":[edge("TRUST-FOUND","M0578-ROOT","trusts","M0578-X-FOUNDATION"),edge("TRUST-PROV","M0578-ROOT","trusts","M0578-X-PROVENANCE")],"documentation":[edge("DOC-MODELS","M0578-S-MODELS","documents","M0578-ROOT"),edge("DOC-SOURCE","M0578-X-SOURCE","documents","M0578-T-PACKAGE")],"workflow":[edge("FLOW-PACK-CONSTR","M0578-T-PACKAGE","workflow_depends_on","M0578-C-BUNDLE"),edge("FLOW-PACK-HOMEO","M0578-T-PACKAGE","workflow_depends_on","M0578-T-HOMEO"),edge("FLOW-PACK-NONDIFF","M0578-T-PACKAGE","workflow_depends_on","M0578-O-NONDIFF"),edge("FLOW-PROV-PACK","M0578-X-PROVENANCE","workflow_depends_on","M0578-T-PACKAGE")]}
graphs={}
for name,edges in edge_sets.items():
 incoming={}; outgoing={}
 for e in edges: outgoing.setdefault(e["from"],[]).append(e["edge_id"]); incoming.setdefault(e["to"],[]).append(e["edge_id"])
 graphs[name]={"edges":edges,"out":outgoing,"in":incoming}
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":ITEM,"theorem_id":THEOREM,"registry_id":"THM-M-0578-OBLIGATIONS-v1","registry_denominator_sha256":denom,"root_node_id":"M0578-ROOT","edge_direction":"Proof requirements run parent to child; reciprocal composes edges run child to parent.","nodes":nodes,"graphs":graphs,"closure_boundary":{"closed_obligations":sorted(checked),"root_closed":False,"audit_complete":False,"theorem_complete":False,"remaining_root_cut_set":["M0578-C-BUNDLE","M0578-T-HOMEO","M0578-O-NONDIFF"],"composition_certificates":["Stage1Instances.THM_M_0578.ObligationTree.root_of_exoticWitnessPackage"],"reason":"Conditional composition only; all three mathematical inputs remain open."}}
specs={"schema_version":"stage1-validation-specs/1.0","item_id":ITEM,"theorem_id":THEOREM,"recipes":[{"recipe_id":"VAL-"+oid,"obligation_id":oid,"command":"python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py","expected_exit":0,"network_policy":"denied"} for oid in ids]}
for name,value in (("obligation-registry.json",registry),("typed-graphs.json",bundle),("validation-specs.json",specs)):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=True)+"\n")
print(denom)
