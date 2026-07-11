#!/usr/bin/env python3
"""Build the frozen THM-M-0404 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0404-OBLIGATION_TREE"
THEOREM = "THM-M-0404"


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("M0404-ROOT", "root", "critical", "The exact characteristic-zero-field Skolem-Mahler-Lech target.", "Stage1Instances.THM_M_0404.SkolemMahlerLechTarget", "The canonical proposition."),
    ("M0404-S-DEFINITIONS", "definition", "high", "Freeze solution, zero predicate, finite exceptions, and one-sided natural progressions, including step zero.", "Stage1Instances.THM_M_0404.{SkolemMahlerLechTarget,IsFiniteUnionOfArithmeticProgressions}", "The exact elaborated statement interface."),
    ("M0404-S-BOUNDARY", "terminal", "high", "Preserve empty, universal, zero-step, order-zero, and identically-zero boundary behavior.", "Stage1Instances.THM_M_0404.{empty_boundary,zero_step_boundary,universal_boundary}", "Checked encoding boundaries; recurrence cases remain proof obligations."),
    ("M0404-S-FOUNDATION", "certificate", "critical", "Fix classical logic, choice, axiom, TCB, and no-oracle policy for every terminal body.", "planned exact foundation and transitive axiom report", "Accepted trust boundary."),
    ("M0404-N-SPECTRAL", "reduction", "critical", "Reduce an arbitrary recurrence solution over its finitely generated coefficient subfield and a splitting extension to a finite exponential-polynomial representation, accounting for repeated roots.", "planned Lean spectral/Jordan reduction for LinearRecurrence.IsSolution", "A finite polynomial-exponential expression agreeing with the sequence."),
    ("M0404-N-TORSION", "normalization", "critical", "Choose a common positive modulus killing every root-of-unity quotient among characteristic roots.", "planned finite root-ratio torsion modulus theorem", "A positive modulus separating torsion-equivalent characteristic roots."),
    ("M0404-B-RESIDUES", "branch", "high", "Partition natural indices into the finitely many residue classes modulo the torsion modulus and prove exhaustiveness.", "planned Nat division residue partition and recomposition", "Exhaustive finite residue-class family."),
    ("M0404-C-SUBSEQUENCES", "construction", "critical", "For each residue class construct the restricted exponential polynomial and prove that distinct surviving base ratios are nontorsion.", "planned residue-subsequence construction with invariants", "One normalized nondegenerate exponential polynomial per residue."),
    ("M0404-L-NONDEGENERATE", "core_lemma", "critical", "A nonzero nondegenerate exponential polynomial over characteristic zero has only finitely many natural zeros.", "planned exact Lean nondegenerate zero-finiteness theorem", "Finiteness of the zeros unless the residual expression is identically zero."),
    ("M0404-B-DICHOTOMY", "branch", "critical", "For each residual expression decide the identically-zero branch or apply nondegenerate zero finiteness, and recompose all branches.", "planned residual identically-zero/finite-zero dichotomy", "Each residue contributes either its full progression or finitely many exceptions."),
    ("M0404-T-EVENTUAL", "terminal", "critical", "Assemble the residue dichotomies into eventual periodicity of the original zero predicate.", "Stage1Instances.THM_M_0404.EventuallyPeriodicZeroSets", "Eventual periodicity for every recurrence solution."),
    ("M0404-L-COMBINATORIAL", "lemma", "high", "Convert any eventually periodic predicate on Nat to finite exceptions plus finitely many one-sided progressions, with positive period and correct initial segment.", "Stage1Instances.THM_M_0404.EventualPeriodicToFiniteUnion", "The predicate-level finite-union representation."),
    ("M0404-T-ASSEMBLE", "transport", "high", "Compose recurrence-specific eventual periodicity and the predicate conversion into the exact canonical target.", "Stage1Instances.THM_M_0404.root_of_eventualPeriodic_packages", "The exact canonical root conditional on both packages."),
    ("M0404-X-SOURCE", "terminal", "high", "Map every material reduction and lemma to reviewed primary-source theorem passages and conventions.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0404-X-PROVENANCE", "certificate", "critical", "Inventory terminal proof bodies, wrappers, imports, axioms, TCB, and replay evidence.", "planned machine-derived provenance and trust closure", "Release provenance coverage without mathematical proof credit."),
]

checked = {"M0404-S-DEFINITIONS", "M0404-S-BOUNDARY", "M0404-T-ASSEMBLE"}
source_na = {"M0404-S-DEFINITIONS", "M0404-S-BOUNDARY", "M0404-S-FOUNDATION", "M0404-X-PROVENANCE"}
machine_special = {"M0404-X-SOURCE": "not_applicable", "M0404-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fp = ("lean-expression-sha256:7b53009924b8101ad44e30b1dfa4367a314fbd142d8834406c146e47201ea3fc"
          if oid in {"M0404-ROOT", "M0404-S-DEFINITIONS"} else "planned:v1:sha256:" + sha([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0404/ObligationTree.lean#root_of_eventualPeriodic_packages" if oid == "M0404-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": "THM-M-0404-" + oid.removeprefix("M0404-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0404-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M0404-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0404-N-SPECTRAL", "M0404-L-NONDEGENERATE"} else 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires children and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0404/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0404-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0404/ObligationTree.lean"] if oid == "M0404-T-ASSEMBLE" else [],
        "owner": "THM-M-0404 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = sha([{k: o[k] for k in fields} for o in obligations])
ids = [o["obligation_id"] for o in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; classical spectral/torsion/nondegenerate architecture; eligibility assigned independently of proof availability.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0404-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0404-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Skolem-Mahler-Lech proof, source acceptance, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0404-ROOT": ["M0404-T-ASSEMBLE"],
    "M0404-T-ASSEMBLE": ["M0404-T-EVENTUAL", "M0404-L-COMBINATORIAL"],
    "M0404-T-EVENTUAL": ["M0404-B-DICHOTOMY"],
    "M0404-B-DICHOTOMY": ["M0404-N-SPECTRAL", "M0404-N-TORSION", "M0404-B-RESIDUES", "M0404-C-SUBSEQUENCES", "M0404-L-NONDEGENERATE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0404-ROOT", "logical_decomposition", "M0404-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M0404-ROOT", "logical_decomposition", "M0404-S-BOUNDARY"), edge("REF-ROOT-FOUND", "M0404-ROOT", "logical_decomposition", "M0404-S-FOUNDATION")],
    "provenance": [edge("SRC-ENGINE", "M0404-L-NONDEGENERATE", "source_map", "M0404-X-SOURCE"), edge("PROV-ROOT", "M0404-X-PROVENANCE", "provenance_of", "M0404-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0404-ROOT", "trusts", "M0404-S-FOUNDATION"), edge("TRUST-PROV", "M0404-ROOT", "trusts", "M0404-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M0404-S-DEFINITIONS", "documents", "M0404-ROOT"), edge("DOC-ENGINE", "M0404-X-SOURCE", "documents", "M0404-L-NONDEGENERATE")],
    "workflow": [edge("FLOW-ASSEMBLE-EVENTUAL", "M0404-T-ASSEMBLE", "workflow_depends_on", "M0404-T-EVENTUAL"), edge("FLOW-ASSEMBLE-COMB", "M0404-T-ASSEMBLE", "workflow_depends_on", "M0404-L-COMBINATORIAL"), edge("FLOW-EVENTUAL-DICH", "M0404-T-EVENTUAL", "workflow_depends_on", "M0404-B-DICHOTOMY"), edge("FLOW-PROV-ASSEMBLE", "M0404-X-PROVENANCE", "workflow_depends_on", "M0404-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0404-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0404-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0404-T-EVENTUAL", "M0404-L-COMBINATORIAL"], "composition_certificates": ["Stage1Instances.THM_M_0404.root_of_eventualPeriodic_packages"], "reason": "The final composition is conditional; neither required input package has a proof body."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0404/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
