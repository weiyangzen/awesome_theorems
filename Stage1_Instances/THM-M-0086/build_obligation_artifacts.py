#!/usr/bin/env python3
"""Build the frozen THM-M-0086 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0086-OBLIGATION_TREE"
PREFIX = "M0086-"
REV = "8a178386"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
 ("ROOT", "root", "critical", "Every abelian category satisfies the embedding, injective-cogenerator, and dual projective-generator branches with their branch-local hypotheses.", "Stage1Instances.THM_M_0086.CanonicalStatement", "The exact frozen three-branch proposition.", "H2", "M1", "R4", 8),
 ("S-EXACT", "definition", "critical", "Fix the exact universes, category and Abelian instances, conjunction association, and branch-local binders.", "Stage1Instances.THM_M_0086.CanonicalStatement", "The exact binder and conjunction boundary.", "H2", "M3", "R3", 16),
 ("S-BOUNDARY", "branch", "high", "Retain empty and degenerate abelian categories without adding Nonempty or nontriviality assumptions.", "Stage1Instances.THM_M_0086.ExcludedBoundaryMutation", "The frozen degenerate-case policy.", "H2", "M3", "R3", 10),
 ("S-TRANSPORT", "transport", "high", "Relate the named branch definitions to the fully unfolded canonical conjunction in both directions.", "Stage1Instances.THM_M_0086.canonicalStatement_iff_unfolded", "Checked equivalence to the unfolded target.", "H2", "M1", "R3", 12),
 ("S-FOUNDATION", "certificate", "high", "Fix classical choice, quotient, propositional extensionality, kernel, and dependency trust boundaries.", "#print axioms terminal declarations and future canonical wrapper", "A versioned foundation and TCB boundary.", "H2", "M3", "R4", 14),
 ("N-CONJ", "normalization", "normal", "Normalize the right-associated conjunction into three independently quantified semantic branches.", "EmbeddingBranch C and InjectiveBranch C and ProjectiveBranch C", "Three non-overlapping branch interfaces.", "H2", "M3", "R3", 12),
 ("B-EMBED", "branch", "critical", "Produce a ring and a full faithful functor preserving finite limits and finite colimits.", "Stage1Instances.THM_M_0086.EmbeddingBranch", "The embedding branch.", "H2", "M1", "R4", 28),
 ("B-INJECTIVE", "branch", "critical", "Under completeness and enough injectives, turn every separator into an injective coseparator.", "Stage1Instances.THM_M_0086.InjectiveBranch", "The injective-cogenerator branch.", "H2", "M1", "R4", 28),
 ("B-PROJECTIVE", "branch", "critical", "Under cocompleteness and enough projectives, turn every coseparator into a projective separator.", "Stage1Instances.THM_M_0086.ProjectiveBranch", "The dual projective-generator branch.", "H2", "M1", "R4", 28),
 ("C-EMBED-FUNCTOR", "construction", "critical", "Construct the Freyd-Mitchell coefficient ring and module-valued embedding functor with its four instances.", "CategoryTheory.Abelian.FreydMitchell.functor", "A full faithful finite-limit and finite-colimit preserving functor.", "H2", "M1", "R4", 80),
 ("C-INJECTIVE", "construction", "critical", "Construct an injective coseparator from the separator, limits, and enough-injectives data.", "CategoryTheory.Abelian.has_injective_coseparator", "An object with Injective and IsCoseparator witnesses.", "H2", "M1", "R4", 80),
 ("C-OPPOSITE", "construction", "critical", "Transport the injective construction through the opposite category and back.", "CategoryTheory.Abelian.has_projective_separator", "A projective separator with dual hypotheses discharged.", "H2", "M1", "R4", 80),
 ("L-EMBED", "core_lemma", "critical", "Package the Freyd-Mitchell construction as the exact embedding existential.", "CategoryTheory.Abelian.freyd_mitchell", "EmbeddingBranch for every abelian category.", "H2", "M1", "R4", 24),
 ("L-INJECTIVE", "core_lemma", "critical", "Package the injective construction as the exact universally quantified branch.", "CategoryTheory.Abelian.has_injective_coseparator", "InjectiveBranch for every abelian category.", "H2", "M1", "R4", 20),
 ("L-PROJECTIVE", "core_lemma", "critical", "Package the opposite-category construction as the exact dual branch.", "CategoryTheory.Abelian.has_projective_separator", "ProjectiveBranch for every abelian category.", "H2", "M1", "R4", 20),
 ("T-ASSEMBLE", "terminal", "critical", "Consume exactly the three branch families and assemble their right-associated conjunction.", "Stage1Instances.THM_M_0086.ObligationTree.root_compose", "The exact root conditional on all branch obligations.", "H2", "M1", "R3", 10),
 ("X-UPSTREAM", "terminal", "high", "Record immutable mathlib terminal bodies, files, declarations, and wrapper/body identities.", "pinned mathlib 8a178386 FreydMitchell and Generator.Abelian", "Body-level formal provenance for all three branches.", "H2", "M3", "R4", 24),
 ("X-SOURCE", "terminal", "critical", "Pinpoint and independently review the primary sources, assumptions, errata, and package identity.", "primary-source crosswalk open", "Human-source mapping for every material branch.", "H2", "M5", "R4", 24),
 ("X-TCB", "terminal", "high", "Audit transitive Lean, mathlib, foundation, imported artifact, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release-grade trust inventory and axiom decision.", "H2", "M3", "R4", 24),
]

def oid(short): return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-UPSTREAM", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "N-CONJ", "X-UPSTREAM", "X-TCB"}
bodies = {
 "S-TRANSPORT": "repo:Stage1Instances.THM_M_0086.canonicalStatement_iff_unfolded",
 "C-EMBED-FUNCTOR": f"mathlib:{REV}:CategoryTheory.Abelian.FreydMitchell.functor",
 "C-INJECTIVE": f"mathlib:{REV}:CategoryTheory.Abelian.has_injective_coseparator",
 "C-OPPOSITE": f"mathlib:{REV}:CategoryTheory.Abelian.has_projective_separator",
 "L-EMBED": f"mathlib:{REV}:CategoryTheory.Abelian.freyd_mitchell",
 "L-INJECTIVE": f"mathlib:{REV}:CategoryTheory.Abelian.has_injective_coseparator",
 "L-PROJECTIVE": f"mathlib:{REV}:CategoryTheory.Abelian.has_projective_separator",
 "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0086.ObligationTree.root_compose",
}
rows=[]
for short,kind,risk,human,formal,output,hd,md,rd,budget in SPECS:
 fp = "lean-expression-sha256:" + expression_hash if short in {"ROOT","S-EXACT"} else "planned:v1:sha256:" + hashlib.sha256((human+"\n"+formal).encode()).hexdigest()
 rows.append({"obligation_id":oid(short),"statement_fingerprint":fp,"kind":kind,"root_relevant":short not in informational,"machine_eligibility":"informational" if short in informational else "required","human_source_eligibility":"not_applicable" if short in no_human else "required","readable_eligibility":"required","risk_class":risk,"exclusion_reason":None,"terminal_proof_body_id":bodies.get(short)})
fields=("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
digest=hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows],sort_keys=True,separators=(",",":")).encode()).hexdigest()
ids=[r["obligation_id"] for r in rows]
registry={"schema_version":"stage1-obligation-registry/1.0","item_id":ITEM,"theorem_id":"THM-M-0086","registry_version":1,"frozen_at":"2026-07-12T00:00:00+08:00","freeze_basis":"The elaborated three-branch target and immutable anchor audit determine the S/N/B/C/L/X/T architecture; eligibility is fixed independently of available closure evidence.","frozen_against_statement_sha256":hashlib.sha256((HERE/"statement.json").read_bytes()).hexdigest(),"frozen_against_anchor_audit_sha256":hashlib.sha256((HERE/"anchor-audit.json").read_bytes()).hexdigest(),"root_obligation_id":oid("ROOT"),"denominator_sha256":digest,"frozen_denominators":{"inventory":ids,"required_machine":[r["obligation_id"] for r in rows if r["machine_eligibility"]=="required"],"required_human_source":[r["obligation_id"] for r in rows if r["human_source_eligibility"]=="required"],"required_readable":ids,"informational_overlays":[r["obligation_id"] for r in rows if r["machine_eligibility"]=="informational"]},"delta_policy":"Any correction, split, merge, eligibility/exclusion/risk change requires registry version 2 and an append-only old/new ID delta.","obligations":rows}

nodes=[]
for spec,row in zip(SPECS,rows):
 short,kind,risk,human,formal,output,hd,md,rd,budget=spec
 nodes.append({"node_id":"THM-M-0086-"+short,"obligation_id":oid(short),"kind":kind,"human_statement":human,"formal_target":formal,"output":output,"human_debt":hd,"machine_debt":md,"readability_debt":rd,"evidence_ids":[],"source_crosswalk_id":"SRC-M0086-PRIMARY-OPEN" if row["human_source_eligibility"]=="required" else "not-applicable","provenance_id":"PROV-M0086-MATHLIB" if short in bodies and short not in {"S-TRANSPORT","T-ASSEMBLE"} else "none","foundation_profile":"Lean 4 kernel plus pinned mathlib; observed axioms propext, Classical.choice, Quot.sound","tcb_profile":"Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open","computation_record":"none","step_budget":budget,"semantic_step_ledger":{"premises":["typed children in proof/refinement graphs"],"inference":formal,"output":output,"outgoing_use":"typed parent edge or root result"},"public_readable_target":"Stage1_Instances/THM-M-0086/obligation-tree.md#"+short.lower(),"validation_spec_id":"VAL-M0086-"+short,"status_boundary":"Architecture only; this obligation is not credited closed or accepted by this phase.","task_ids":[ITEM,"S56-M-0086-PROOF"],"owned_sources":["Stage1_Instances/THM-M-0086/obligation-registry.json","Stage1_Instances/THM-M-0086/typed-graphs.json"],"owner":"Stage1 execution worker","reviewer":"independent integration lane","validity":{"validated_at":"2026-07-12","review_due":"before master acceptance","invalidation_inputs":["statement","registry","toolchain","mathlib revision","anchor provenance"],"revocation_state":"not-accepted"}})

def graph(edges):
 out,inc={},{}
 for e in edges: out.setdefault(e["from"],[]).append(e["edge_id"]); inc.setdefault(e["to"],[]).append(e["edge_id"])
 return {"edges":edges,"out":out,"in":inc}

pairs=[("ROOT","T-ASSEMBLE"),("T-ASSEMBLE","L-EMBED"),("T-ASSEMBLE","L-INJECTIVE"),("T-ASSEMBLE","L-PROJECTIVE"),("L-EMBED","B-EMBED"),("L-EMBED","C-EMBED-FUNCTOR"),("L-INJECTIVE","B-INJECTIVE"),("L-INJECTIVE","C-INJECTIVE"),("L-PROJECTIVE","B-PROJECTIVE"),("L-PROJECTIVE","C-OPPOSITE")]
proof=[]
for a,b in pairs:
 f,r=f"PROOF-{a}-{b}",f"COMPOSE-{b}-{a}"
 proof += [{"edge_id":f,"from":oid(a),"type":"proof_requires","to":oid(b),"reciprocal_edge_id":r},{"edge_id":r,"from":oid(b),"type":"composes","to":oid(a),"reciprocal_edge_id":f}]
refpairs=[("ROOT","S-EXACT"),("S-EXACT","S-BOUNDARY"),("S-EXACT","S-TRANSPORT"),("S-EXACT","S-FOUNDATION"),("ROOT","N-CONJ"),("N-CONJ","B-EMBED"),("N-CONJ","B-INJECTIVE"),("N-CONJ","B-PROJECTIVE")]
provnodes=("C-EMBED-FUNCTOR","C-INJECTIVE","C-OPPOSITE","L-EMBED","L-INJECTIVE","L-PROJECTIVE")
graphs={"proof":graph(proof),"refinement":graph([{"edge_id":f"REFINE-{a}-{b}","from":oid(a),"type":"logical_decomposition","to":oid(b)} for a,b in refpairs]),"provenance":graph([{"edge_id":f"PROV-{s}","from":oid(s),"type":"provenance_of","to":oid("X-UPSTREAM")} for s in provnodes]+[{"edge_id":f"SOURCE-{s}","from":oid(s),"type":"source_map","to":oid("X-SOURCE")} for s in ("ROOT","B-EMBED","B-INJECTIVE","B-PROJECTIVE")]),"evidence":graph([{"edge_id":"EVID-ROOT-UPSTREAM","from":oid("ROOT"),"type":"evidence_for","to":oid("X-UPSTREAM")}]),"trust":graph([{"edge_id":"TRUST-ROOT-TCB","from":oid("ROOT"),"type":"trusts","to":oid("X-TCB")}]),"documentation":graph([{"edge_id":"DOC-ROOT-SOURCE","from":oid("ROOT"),"type":"documents","to":oid("X-SOURCE")}]),"workflow":graph([{"edge_id":"FLOW-ROOT-ASSEMBLE","from":oid("ROOT"),"type":"workflow_depends_on","to":oid("T-ASSEMBLE")}])}
bundle={"schema_version":"stage1-typed-graphs/1.0","item_id":ITEM,"theorem_id":"THM-M-0086","registry_denominator_sha256":digest,"nodes":nodes,"graphs":graphs,"closure_boundary":{"closed_obligations":[],"root_closed":False,"root_machine_debt":"M1","remaining_root_cut_set":[oid("L-EMBED"),oid("L-INJECTIVE"),oid("L-PROJECTIVE")],"composition_certificates_checked":["Stage1Instances.THM_M_0086.ObligationTree.root_compose"],"audit_complete":False,"theorem_complete":False}}
recipes=[{"recipe_id":"VAL-M0086-"+s[0],"cwd":"Formalizations/Lean","argv":["lake","env","lean","../../Stage1_Instances/THM-M-0086/ObligationTree.lean"],"env":{},"timeout_seconds":120,"network":"forbidden","covered_ids":[oid(s[0])]} for s in SPECS]
validation={"schema_version":"stage1-validation-specs/1.0","item_id":ITEM,"theorem_id":"THM-M-0086","recipes":recipes}
for name,value in (("obligation-registry.json",registry),("typed-graphs.json",bundle),("validation-specs.json",validation)):
 (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=True)+"\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {digest}")
