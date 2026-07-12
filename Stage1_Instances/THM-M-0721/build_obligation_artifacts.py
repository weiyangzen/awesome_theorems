#!/usr/bin/env python3
"""Build the deterministic THM-M-0721 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def planned(text): return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()

# id, kind, statement, output, risk, machine, human-source, formal target, debt
ROWS = [
 ("M0721-ROOT", "root", "There exists a binary-word language in the frozen verifier-based NP that is polynomial-time many-one hard for every such NP language.", "Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage", "critical", "required", "required", "Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage", "M3"),
 ("M0721-S-DEFINITIONS", "definition", "Freeze Word, Language, encodings, verifier-based InNP, TM2 polynomial time, reductions, and NPComplete.", "The elaborated statement interface and its exact encodings.", "high", "required", "not_applicable", "Stage1Instances.THM_M_0721.{Word,Language,encodePair,InNP,PolyManyOneReducible,NPComplete}", "M0-L"),
 ("M0721-S-BOUNDARY", "terminal", "Preserve the binary alphabet, empty input and certificate, separator pairing, and zero-bound behavior.", "Checked encoding boundary facts.", "high", "required", "not_applicable", "Stage1Instances.THM_M_0721.{binary_alphabet_has_two_distinct_symbols,encodePair_empty_empty,empty_certificate_is_in_boundary}", "M0-L"),
 ("M0721-S-FOUNDATION", "certificate", "Audit classical principles, terminal axioms, imports, TCB, and the no-oracle policy.", "An accepted transitive foundation and trust report.", "critical", "required", "not_applicable", "planned exact axiom and transitive import report", "M4"),
 ("M0721-N-SAT-ENCODING", "normalization", "Define faithful Boolean formula syntax plus total binary encoders and decoders for formulas, assignments, and verifier pairs.", "A concrete binary-word satisfiability language with encoding invariants.", "critical", "required", "required", "planned Lean SAT syntax, encoding, decoding, and round-trip signatures", "M4"),
 ("M0721-C-SAT-VERIFIER", "construction", "Construct the deterministic TM2 verifier that decodes a formula and assignment and evaluates satisfaction.", "A verifier function and implementing machine.", "critical", "required", "required", "planned TM2 verifier construction", "M4"),
 ("M0721-L-SAT-CORRECT", "core_lemma", "Prove the verifier accepts exactly the satisfying assignments of the decoded formula.", "Verifier soundness and completeness for SAT membership.", "critical", "required", "required", "planned verifier correctness theorem", "M4"),
 ("M0721-L-SAT-RUNTIME", "core_lemma", "Prove the SAT verifier TM2 runs in polynomial time under the frozen pair encoding.", "TM2ComputableInPolyTime evidence for the verifier.", "critical", "required", "required", "planned verifier runtime theorem", "M4"),
 ("M0721-T-SAT-IN-NP", "terminal", "Assemble decoding, certificate length, verifier correctness, and runtime into InNP for the candidate language.", "CandidateMembership for the chosen SAT language.", "critical", "required", "required", "planned Stage1Instances.THM_M_0721.sat_in_np", "M4"),
 ("M0721-N-MACHINE-NORMALIZE", "normalization", "Normalize an arbitrary frozen InNP verifier, its polynomial certificate bound, and input into a bounded computation instance.", "A uniform bounded TM2 computation description.", "critical", "required", "required", "planned verifier-to-bounded-computation normalization", "M4"),
 ("M0721-C-TABLEAU", "construction", "Construct variables and local constraints encoding the normalized accepting computation tableau.", "A finite tableau constraint system with well-formed indices and local invariants.", "critical", "required", "required", "planned Cook-Levin tableau construction", "M4"),
 ("M0721-L-TABLEAU-SOUND", "core_lemma", "Decode any satisfying tableau assignment into an accepting verifier computation and a certificate within the frozen bound.", "Formula satisfiability implies source-language membership.", "critical", "required", "required", "planned tableau soundness theorem", "M4"),
 ("M0721-L-TABLEAU-COMPLETE", "core_lemma", "Encode any bounded accepting verifier computation as a satisfying tableau assignment.", "Source-language membership implies formula satisfiability.", "critical", "required", "required", "planned tableau completeness theorem", "M4"),
 ("M0721-L-REDUCTION-RUNTIME", "core_lemma", "Prove construction and binary serialization of the tableau formula are performed by a TM2 in polynomial time.", "PolytimeFunction evidence for the reduction.", "critical", "required", "required", "planned Cook-Levin reduction runtime theorem", "M4"),
 ("M0721-T-UNIVERSAL-HARDNESS", "terminal", "For every frozen InNP source, assemble the tableau construction, two correctness directions, and runtime into a many-one reduction to SAT.", "CandidateHardness for the same candidate language.", "critical", "required", "required", "planned Stage1Instances.THM_M_0721.sat_hard", "M4"),
 ("M0721-T-ASSEMBLE", "transport", "Combine candidate membership and universal hardness without adding a premise.", "The exact existential NP-completeness target.", "high", "required", "required", "Stage1Instances.THM_M_0721.root_of_candidate_packages", "M0-L"),
 ("M0721-X-SOURCE", "terminal", "Pin primary Cook-Levin and NP-completeness sources and map each proof node to exact assumptions and proof passages.", "Human-source coverage; no machine proof credit.", "high", "not_applicable", "required", "planned primary-source node crosswalk", "M4"),
 ("M0721-X-PROVENANCE", "certificate", "Inventory terminal bodies, wrappers, imports, placeholders, axioms, and replay evidence.", "Release provenance coverage; no mathematical proof credit.", "critical", "informational", "not_applicable", "planned terminal-body provenance ledger", "M4"),
]

obligations=[]
for oid, kind, statement, output, risk, mach, human, formal, debt in ROWS:
    obligations.append({"obligation_id":oid,"statement_fingerprint":("lean-expression-sha256:758b1033903c92b231a24ae3fb5e01e0bbb0d6fdb0bc41f809c062deb7b4b204" if oid=="M0721-ROOT" else planned(formal)),"kind":kind,"root_relevant":True,"machine_eligibility":mach,"human_source_eligibility":human,"readable_eligibility":"required","risk_class":risk,"exclusion_reason":({"not_applicable":"human_source_boundary_only","informational":"release_provenance_overlay_no_proof_credit"}.get(mach)),"terminal_proof_body_id":("local:Stage1_Instances/THM-M-0721/ObligationTree.lean#root_of_candidate_packages" if oid=="M0721-T-ASSEMBLE" else None)})
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
projection=[{k:r[k] for k in fields} for r in obligations]
digest=hashlib.sha256(json.dumps(projection,sort_keys=True,separators=(",",":")).encode()).hexdigest()
ids=[r[0] for r in ROWS]
registry={"schema_version":"stage1-obligation-registry/1.0","item_id":"S56-M-0721-OBLIGATION_TREE","theorem_id":"THM-M-0721","registry_version":1,"frozen_at":"2026-07-12T00:00:00+08:00","freeze_basis":"Exact binary-word verifier statement and immutable anchor audit; SAT/Cook-Levin architecture selected before proof status is credited.","frozen_against_statement_sha256":sha(HERE/"Statement.lean"),"frozen_against_anchor_audit_sha256":sha(HERE/"anchor-audit.json"),"root_obligation_id":"M0721-ROOT","denominator_sha256":digest,"frozen_denominators":{"inventory":ids,"required_machine":[r[0] for r in ROWS if r[5]=="required"],"required_human_source":[r[0] for r in ROWS if r[6]=="required"],"required_readable":ids,"informational_overlays":["M0721-X-PROVENANCE"]},"delta_policy":"Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.","obligations":obligations,"append_only_delta":[],"status_observed_after_freeze":{"closed_obligations":["M0721-S-DEFINITIONS","M0721-S-BOUNDARY","M0721-T-ASSEMBLE"],"root_machine_debt":"M3"},"status_boundary":"Architecture and frozen denominators only; no SAT membership, Cook-Levin reduction, source H0, or theorem completion."}

nodes=[]
for oid,kind,statement,output,risk,mach,human,formal,debt in ROWS:
    nodes.append({"node_id":"THM-M-0721-"+oid.removeprefix("M0721-"),"obligation_id":oid,"kind":kind,"human_statement":statement,"formal_target":formal,"output":output,"human_debt":"H1","machine_debt":debt,"readability_debt":"R4","evidence_ids":[],"source_crosswalk_id":("not-applicable" if human=="not_applicable" else "primary-source-node-map-pending"),"provenance_id":("local-conditional-composition" if oid=="M0721-T-ASSEMBLE" else "none"),"foundation_profile":"lean4-mathlib/policy-audit-pending","tcb_profile":"lean-4.29.0+mathlib-8a178386/transitive-closure-pending","computation_record":"none; no oracle, native computation, or external solver may close this node","step_budget":100 if risk=="critical" else 40,"semantic_step_ledger":{"premises":"Only exact incoming proof_requires children and the stated formal context.","inference":statement,"output":output,"outgoing_use":"Only the declared typed parent or non-proof support edge may consume this output."},"public_readable_target":f"Stage1_Instances/THM-M-0721/obligation-tree.md#{oid.lower()}","validation_spec_id":"VAL-"+oid,"status_boundary":"Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.","task_ids":["S56-M-0721-OBLIGATION_TREE","S56-M-0721-PROOF"],"owned_sources":(["Stage1_Instances/THM-M-0721/ObligationTree.lean"] if oid=="M0721-T-ASSEMBLE" else []),"owner":"THM-M-0721 proof lane","reviewer":"independent Stage1 integration lane","validity":{"validated_at":("2026-07-12" if debt=="M0-L" else None),"review_due":"before proof acceptance","invalidation_inputs":["statement","registry","source map","toolchain"],"revocation_state":("provisional" if debt=="M0-L" else "open")}})

proof_pairs=[("M0721-ROOT","M0721-T-ASSEMBLE"),("M0721-T-ASSEMBLE","M0721-T-SAT-IN-NP"),("M0721-T-ASSEMBLE","M0721-T-UNIVERSAL-HARDNESS"),("M0721-T-SAT-IN-NP","M0721-N-SAT-ENCODING"),("M0721-T-SAT-IN-NP","M0721-C-SAT-VERIFIER"),("M0721-T-SAT-IN-NP","M0721-L-SAT-CORRECT"),("M0721-T-SAT-IN-NP","M0721-L-SAT-RUNTIME"),("M0721-T-UNIVERSAL-HARDNESS","M0721-N-MACHINE-NORMALIZE"),("M0721-T-UNIVERSAL-HARDNESS","M0721-C-TABLEAU"),("M0721-T-UNIVERSAL-HARDNESS","M0721-L-TABLEAU-SOUND"),("M0721-T-UNIVERSAL-HARDNESS","M0721-L-TABLEAU-COMPLETE"),("M0721-T-UNIVERSAL-HARDNESS","M0721-L-REDUCTION-RUNTIME")]
def graph(edges):
    out={}; inn={}
    for e in edges: out.setdefault(e["from"],[]).append(e["edge_id"]); inn.setdefault(e["to"],[]).append(e["edge_id"])
    return {"edges":edges,"out":out,"in":inn}
pedges=[]
for p,c in proof_pairs:
    a=f"REQ-{p}-{c}"; b=f"CMP-{c}-{p}"
    pedges += [{"edge_id":a,"from":p,"type":"proof_requires","to":c,"reciprocal_edge_id":b},{"edge_id":b,"from":c,"type":"composes","to":p,"reciprocal_edge_id":a}]
ref=[{"edge_id":f"REF-ROOT-{x}","from":"M0721-ROOT","type":"logical_decomposition","to":x} for x in ("M0721-S-DEFINITIONS","M0721-S-BOUNDARY","M0721-S-FOUNDATION")]
prov=[{"edge_id":"SRC-COOK-LEVIN","from":"M0721-T-UNIVERSAL-HARDNESS","type":"source_map","to":"M0721-X-SOURCE"},{"edge_id":"PROV-ROOT","from":"M0721-X-PROVENANCE","type":"provenance_of","to":"M0721-ROOT"}]
trust=[{"edge_id":"TRUST-FOUND","from":"M0721-ROOT","type":"trusts","to":"M0721-S-FOUNDATION"},{"edge_id":"TRUST-PROV","from":"M0721-ROOT","type":"trusts","to":"M0721-X-PROVENANCE"}]
docs=[{"edge_id":"DOC-DEFS","from":"M0721-S-DEFINITIONS","type":"documents","to":"M0721-ROOT"},{"edge_id":"DOC-SOURCE","from":"M0721-X-SOURCE","type":"documents","to":"M0721-T-UNIVERSAL-HARDNESS"}]
flows=[{"edge_id":f"FLOW-{p}-{c}","from":p,"type":"workflow_depends_on","to":c} for p,c in proof_pairs]
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":"S56-M-0721-OBLIGATION_TREE","theorem_id":"THM-M-0721","registry_id":"THM-M-0721-OBLIGATIONS-v1","registry_denominator_sha256":digest,"root_node_id":"M0721-ROOT","edge_direction":"Proof requirements run parent to child; reciprocal composes edges run child to parent.","nodes":nodes,"graphs":{"proof":graph(pedges),"refinement":graph(ref),"provenance":graph(prov),"evidence":graph([]),"trust":graph(trust),"documentation":graph(docs),"workflow":graph(flows)},"closure_boundary":{"closed_obligations":["M0721-S-DEFINITIONS","M0721-S-BOUNDARY","M0721-T-ASSEMBLE"],"root_closed":False,"audit_complete":False,"theorem_complete":False,"remaining_root_cut_set":["M0721-T-SAT-IN-NP","M0721-T-UNIVERSAL-HARDNESS"],"composition_certificates":["Stage1Instances.THM_M_0721.root_of_candidate_packages"],"reason":"Final composition is conditional; neither candidate membership nor universal hardness has a proof body."}}
spec={"schema_version":"stage1-validation-specs/1.0","item_id":"S56-M-0721-OBLIGATION_TREE","theorem_id":"THM-M-0721","recipes":[{"recipe_id":"VAL-"+oid,"obligation_id":oid,"command":"python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py","expected_exit":0,"network_policy":"denied"} for oid in ids]}

for name,obj in (("obligation-registry.json",registry),("typed-graphs.json",bundle),("validation-specs.json",spec)):
    (HERE/name).write_text(json.dumps(obj,indent=2)+"\n")

lines=["# THM-M-0721 frozen obligation tree","","This is an architecture freeze, not an NP-completeness proof. All open semantic packages remain `unchecked`.",""]
for n in nodes:
    lines += [f"## {n['obligation_id'].lower()}","",f"**{n['human_statement']}**", "",f"Formal target: `{n['formal_target']}`  ",f"Debt: `{n['human_debt']} / {n['machine_debt']} / {n['readability_debt']}`; budget: `{n['step_budget']}`; state: `{'provisional checked interface' if n['machine_debt']=='M0-L' else 'unchecked'}`.","",f"Output: {n['output']}","",f"Boundary: {n['status_boundary']}",""]
(HERE/"obligation-tree.md").write_text("\n".join(lines)+"\n")
print(f"built {len(ids)} obligations; denominator {digest}")
