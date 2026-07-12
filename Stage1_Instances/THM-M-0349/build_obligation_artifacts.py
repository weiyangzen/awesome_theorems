#!/usr/bin/env python3
"""Generate the frozen THM-M-0349 registry and typed graph bundle."""
import hashlib, json
from pathlib import Path

H = Path(__file__).resolve().parent
ids = [
  "M0349-ROOT", "M0349-T-ASSEMBLE", "M0349-P-EXISTENCE", "M0349-P-BOUND",
  "M0349-D-DENSE", "M0349-C-POLYNOMIAL", "M0349-L-WEAK11", "M0349-L-L2",
  "M0349-L-INTERPOLATE", "M0349-C-EXTEND", "M0349-L-FOURIER-ID",
  "M0349-S-ENDPOINTS", "M0349-X-SOURCE", "M0349-X-TRUST", "M0349-X-PROVENANCE"]
desc = {
 "M0349-ROOT": ("root", "Exact periodic conjugate-function target", "Stage1Instances.THM_M_0349.ConjugateFunctionTheoremTarget", "M3", 40),
 "M0349-T-ASSEMBLE": ("transport", "Compose existence and uniform-bound packages", "Stage1Instances.THM_M_0349.root_of_conjugate_packages", "M0-L", 20),
 "M0349-P-EXISTENCE": ("package", "Construct an Lp conjugate for every admissible f", "Stage1Instances.THM_M_0349.ConjugateExistencePackage", "M4", 60),
 "M0349-P-BOUND": ("package", "Choose one nonnegative bound depending only on p", "Stage1Instances.THM_M_0349.ConjugateUniformBoundPackage", "M4", 60),
 "M0349-D-DENSE": ("bridge", "Use Fourier polynomials as a dense finite-exponent subspace", "planned exact dense-subspace theorem", "M4", 60),
 "M0349-C-POLYNOMIAL": ("construction", "Define the sign multiplier on Fourier polynomials", "planned exact polynomial conjugation operator", "M4", 60),
 "M0349-L-WEAK11": ("core_lemma", "Prove the weak (1,1) estimate for truncated conjugate kernels", "planned exact weak-type estimate", "M4", 100),
 "M0349-L-L2": ("core_lemma", "Prove the L2 multiplier bound by Fourier orthogonality", "planned exact L2 estimate", "M4", 80),
 "M0349-L-INTERPOLATE": ("core_lemma", "Interpolate and dualize to all 1 < p < infinity", "planned exact strong-type estimate", "M4", 100),
 "M0349-C-EXTEND": ("construction", "Extend the bounded polynomial operator uniquely to Lp", "planned exact continuous extension theorem", "M4", 80),
 "M0349-L-FOURIER-ID": ("bridge", "Identify Fourier coefficients of the Lp extension", "planned exact Fourier-coefficient identity", "M4", 80),
 "M0349-S-ENDPOINTS": ("boundary", "Preserve strict endpoints, zero mode, circle and measure conventions", "Statement.lean structural boundary", "M0-L", 30),
 "M0349-X-SOURCE": ("source", "Pin a primary proof and map every analytic node", "primary-source node map pending", "M4", 40),
 "M0349-X-TRUST": ("certificate", "Inventory axioms, imports, TCB and no-oracle policy", "planned trust certificate", "M4", 40),
 "M0349-X-PROVENANCE": ("certificate", "Track terminal bodies and immutable evidence", "planned provenance certificate", "M4", 40)}
machine_na = {"M0349-X-SOURCE"}; info = {"M0349-X-PROVENANCE"}
rows=[]
for i in ids:
 k,human,formal,mdebt,budget=desc[i]
 fp=hashlib.sha256(("THM-M-0349:v1:"+i+":"+human+":"+formal).encode()).hexdigest()
 rows.append({"obligation_id":i,"statement_fingerprint":"planned:v1:sha256:"+fp,"kind":k,
  "root_relevant":True,"machine_eligibility":"not_applicable" if i in machine_na else ("informational" if i in info else "required"),
  "human_source_eligibility":"required" if i not in {"M0349-S-ENDPOINTS","M0349-X-TRUST","M0349-X-PROVENANCE"} else "not_applicable",
  "readable_eligibility":"required","risk_class":"critical" if i in {"M0349-ROOT","M0349-L-WEAK11","M0349-L-INTERPOLATE","M0349-X-TRUST"} else "high",
  "exclusion_reason":"human_source_boundary_only" if i in machine_na else ("provenance_overlay_no_proof_credit" if i in info else None),
  "terminal_proof_body_id":"local:Stage1_Instances/THM-M-0349/ObligationTree.lean#root_of_conjugate_packages" if i=="M0349-T-ASSEMBLE" else None})
fields=tuple(rows[0]); digest=hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows],sort_keys=True,separators=(",",":")).encode()).hexdigest()
reg={"schema_version":"stage1-obligation-registry/1.0","item_id":"S56-M-0349-OBLIGATION_TREE","theorem_id":"THM-M-0349","registry_version":1,
 "frozen_at":"2026-07-12T00:00:00+08:00","freeze_basis":"Exact elaborated statement plus bounded anchor audit; classical weak-type/interpolation route, frozen independently of proof availability.",
 "frozen_against_statement_sha256":hashlib.sha256((H/"Statement.lean").read_bytes()).hexdigest(),"frozen_against_anchor_audit_sha256":hashlib.sha256((H/"anchor-audit.json").read_bytes()).hexdigest(),
 "root_obligation_id":ids[0],"denominator_sha256":digest,"frozen_denominators":{"inventory":ids,"required_machine":[r["obligation_id"] for r in rows if r["machine_eligibility"]=="required"],"required_human_source":[r["obligation_id"] for r in rows if r["human_source_eligibility"]=="required"],"required_readable":ids,"informational_overlays":["M0349-X-PROVENANCE"]},
 "delta_policy":"Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.","obligations":rows}
proof_children={"M0349-ROOT":["M0349-T-ASSEMBLE"],"M0349-T-ASSEMBLE":["M0349-P-EXISTENCE","M0349-P-BOUND"],"M0349-P-EXISTENCE":["M0349-C-EXTEND","M0349-L-FOURIER-ID"],"M0349-P-BOUND":["M0349-L-INTERPOLATE","M0349-C-EXTEND"],"M0349-C-EXTEND":["M0349-D-DENSE","M0349-C-POLYNOMIAL"],"M0349-L-FOURIER-ID":["M0349-D-DENSE","M0349-C-POLYNOMIAL"],"M0349-L-INTERPOLATE":["M0349-L-WEAK11","M0349-L-L2"]}
def edges(pairs, typ): return [{"edge_id":f"{typ}:{a}:{b}","type":typ,"from":a,"to":b} for a,b in pairs]
pe=[]
for p,cs in proof_children.items():
 for c in cs:
  a={"edge_id":f"requires:{p}:{c}","type":"proof_requires","from":p,"to":c,"reciprocal_edge_id":f"composes:{c}:{p}"}; b={"edge_id":f"composes:{c}:{p}","type":"composes","from":c,"to":p,"reciprocal_edge_id":a["edge_id"]}; pe += [a,b]
graphs={"proof":{"edges":pe},"refinement":{"edges":edges([("M0349-S-ENDPOINTS","M0349-ROOT")],"logical_decomposition")},"provenance":{"edges":edges([("M0349-X-PROVENANCE",i) for i in ids if i!="M0349-X-PROVENANCE"],"provenance_of")},"evidence":{"edges":[]},"trust":{"edges":edges([("M0349-X-TRUST",i) for i in ids if i!="M0349-X-TRUST"],"trusts")},"documentation":{"edges":edges([("M0349-X-SOURCE",i) for i in ids if i not in {"M0349-X-SOURCE","M0349-X-TRUST","M0349-X-PROVENANCE","M0349-S-ENDPOINTS"}],"source_map")},"workflow":{"edges":edges([("M0349-T-ASSEMBLE","M0349-ROOT"), ("M0349-X-TRUST","M0349-T-ASSEMBLE"), ("M0349-X-PROVENANCE","M0349-T-ASSEMBLE")],"workflow_depends_on")}}
for g in graphs.values():
 g["out"]={i:[e["edge_id"] for e in g["edges"] if e["from"]==i] for i in ids}; g["in"]={i:[e["edge_id"] for e in g["edges"] if e["to"]==i] for i in ids}
nodes=[]
for i in ids:
 k,human,formal,mdebt,budget=desc[i]
 nodes.append({"node_id":"THM-M-0349-"+i[6:],"obligation_id":i,"kind":k,"human_statement":human,"formal_target":formal,"output":human,"human_debt":"H3","machine_debt":mdebt,"readability_debt":"R4","evidence_ids":[],"source_crosswalk_id":"primary-source-node-map-pending" if i not in {"M0349-S-ENDPOINTS","M0349-X-TRUST","M0349-X-PROVENANCE"} else "not-applicable","provenance_id":"none","foundation_profile":"lean4-mathlib-classical/policy-audit-pending","tcb_profile":"lean-4.29.0+mathlib-8a178386/transitive-closure-pending","computation_record":"none; no oracle or unchecked computation may close this node","step_budget":budget,"semantic_step_ledger":{"premises":"Only declared proof-requirement children and the formal context.","inference":human,"output":human,"outgoing_use":"Only declared typed edges may consume this output."},"public_readable_target":"Stage1_Instances/THM-M-0349/obligation-tree.md#"+i.lower(),"validation_spec_id":"VAL-"+i,"status_boundary":"Frozen interface only; open premises receive no proof credit.","task_ids":["S56-M-0349-OBLIGATION_TREE","S56-M-0349-PROOF"],"owned_sources":[],"owner":"THM-M-0349 proof lane","reviewer":"independent Stage1 integration lane","validity":{"validated_at":"2026-07-12" if mdebt=="M0-L" else None,"review_due":"before proof acceptance","invalidation_inputs":["statement","registry","source map","toolchain"],"revocation_state":"provisional" if mdebt=="M0-L" else "open"}})
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":"S56-M-0349-OBLIGATION_TREE","theorem_id":"THM-M-0349","registry_id":"THM-M-0349-OBLIGATIONS-v1","registry_denominator_sha256":digest,"root_node_id":ids[0],"edge_direction":"proof_requires parent to child; composes child to parent","nodes":nodes,"graphs":graphs,"closure_boundary":{"root_closed":False,"theorem_complete":False,"minimal_open_root_cut":["M0349-P-EXISTENCE","M0349-P-BOUND"]}}
(H/"obligation-registry.json").write_text(json.dumps(reg,indent=2)+"\n"); (H/"typed-graphs.json").write_text(json.dumps(bundle,indent=2)+"\n")
print(digest)
