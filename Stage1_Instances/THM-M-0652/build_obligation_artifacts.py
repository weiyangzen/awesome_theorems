#!/usr/bin/env python3
"""Build the frozen THM-M-0652 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0652-OBLIGATION_TREE"
THEOREM = "THM-M-0652"

# ID, kind, claim, formal target, output, risk, machine, human, readable, budget
SPECS = [
    ("M0652-ROOT", "root", "Prove the exact semantic sentence-level Craig interpolation target.", "Stage1Instances.THM_M_0652.Statement", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M0652-S-DEFINITIONS", "definition", "Preserve semantic entailment and exact occurrence-subset vocabulary.", "Stage1Instances.THM_M_0652.{SentenceEntails,UsesOnlyCommonVocabulary,IsInterpolant}", "The frozen statement interface.", "critical", "required", "not_applicable", "required", 30),
    ("M0652-S-BOUNDARY", "terminal", "Cover empty and identical vocabularies and sentences with no nonlogical symbols.", "planned exact boundary lemmas", "Boundary cases without extra language assumptions.", "high", "required", "required", "required", 40),
    ("M0652-S-FOUNDATION", "certificate", "Audit classical principles, quotient use, imports, and the transitive TCB.", "planned axiom and trust report", "Accepted foundation profile.", "critical", "required", "not_applicable", "required", 40),
    ("M0652-N-CALCULUS", "normalization", "Define a sound first-order sequent calculus matching mathlib sentences and semantics.", "planned exact DerivationRelation implementation", "A derivability relation with formula/language transports.", "critical", "required", "required", "required", 100),
    ("M0652-B-COMPLETENESS", "bridge", "Turn semantic entailment into derivability without strengthening the context.", "Stage1Instances.THM_M_0652.SemanticCompleteness", "Derivation of psi from phi.", "critical", "required", "required", "required", 100),
    ("M0652-B-SOUNDNESS", "bridge", "Turn each extracted derivation back into mathlib semantic entailment.", "Stage1Instances.THM_M_0652.DerivationSoundness", "Both semantic entailment legs.", "critical", "required", "required", "required", 80),
    ("M0652-C-CUTFREE", "construction", "Normalize the endpoint derivation to a cut-free derivation preserving symbols.", "planned cut-elimination theorem", "A cut-free derivation suitable for induction.", "critical", "required", "required", "required", 100),
    ("M0652-L-MAEHARA", "core_lemma", "Induct over the cut-free derivation and construct an interpolant for every rule.", "planned Maehara lemma", "A syntactic interpolant and two derivations.", "critical", "required", "required", "required", 100),
    ("M0652-L-VOCAB", "lemma", "Relate calculus symbol occurrence to the frozen forall-support predicate.", "planned occurrence/support equivalence", "UsesOnlyCommonVocabulary for the extracted sentence.", "critical", "required", "required", "required", 80),
    ("M0652-T-SYNTACTIC", "terminal", "Combine cut elimination, Maehara induction, and support transport.", "Stage1Instances.THM_M_0652.SyntacticInterpolation", "The full syntactic interpolation package.", "critical", "required", "required", "required", 50),
    ("M0652-T-ASSEMBLE", "transport", "Compose completeness, interpolation, and soundness into the exact root.", "Stage1Instances.THM_M_0652.statement_of_calculus_packages", "Statement conditional on three explicit packages.", "high", "required", "required", "required", 20),
    ("M0652-X-SOURCE", "terminal", "Pin a primary proof and crosswalk every material inference.", "human source boundary; no Lean proposition", "Reviewed node-level source crosswalk.", "high", "not_applicable", "required", "required", 60),
    ("M0652-X-PROVENANCE", "certificate", "Classify every terminal proof body and imported bridge by immutable origin.", "planned proof-body provenance closure", "Content-addressed provenance.", "critical", "informational", "not_applicable", "required", 50),
    ("M0652-X-TRUST", "certificate", "Record automation, executable, compiled-artifact, dependency, and computation trust.", "planned release trust record", "Replayable trust boundary.", "critical", "informational", "not_applicable", "required", 50),
]

def planned_fingerprint(oid, target):
    if oid == "M0652-ROOT":
        return "lean-expression-sha256:31ddfe8d7d426cacfb1acb17e443bbaa59a0e975fb92fb47916a600964362c6a"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations, nodes = [], []
for oid, kind, claim, target, output, risk, machine, human, readable, budget in SPECS:
    closed = oid in {"M0652-S-DEFINITIONS", "M0652-T-ASSEMBLE"}
    body = "local:Stage1_Instances/THM-M-0652/ObligationTree.lean#statement_of_calculus_packages" if oid == "M0652-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": planned_fingerprint(oid, target),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0652-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == "M0652-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the formal context and declared proof_requires children.", "inference": claim, "output": output, "outgoing_use": "Only declared composition or non-proof support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0652/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise or root closure.",
        "task_ids": [ITEM, "S56-M-0652-PROOF"], "owned_sources": [],
        "owner": "THM-M-0652 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; completeness plus cut elimination/Maehara extraction route selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0652-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"], "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0652-S-DEFINITIONS", "M0652-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; completeness, calculus, interpolation extraction, source, and trust remain open.",
}

pairs = [("M0652-ROOT", "M0652-T-ASSEMBLE"), ("M0652-T-ASSEMBLE", "M0652-B-COMPLETENESS"), ("M0652-T-ASSEMBLE", "M0652-T-SYNTACTIC"), ("M0652-T-ASSEMBLE", "M0652-B-SOUNDNESS"), ("M0652-B-COMPLETENESS", "M0652-N-CALCULUS"), ("M0652-B-SOUNDNESS", "M0652-N-CALCULUS"), ("M0652-T-SYNTACTIC", "M0652-C-CUTFREE"), ("M0652-T-SYNTACTIC", "M0652-L-MAEHARA"), ("M0652-T-SYNTACTIC", "M0652-L-VOCAB"), ("M0652-C-CUTFREE", "M0652-N-CALCULUS"), ("M0652-L-MAEHARA", "M0652-C-CUTFREE"), ("M0652-L-VOCAB", "M0652-S-DEFINITIONS"), ("M0652-N-CALCULUS", "M0652-S-BOUNDARY")]
proof = []
for parent, child in pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]
other = {
    "refinement": [("REF-ROOT-DEFS", "M0652-ROOT", "logical_decomposition", "M0652-S-DEFINITIONS")],
    "provenance": [("SRC-COMP", "M0652-B-COMPLETENESS", "source_map", "M0652-X-SOURCE"), ("SRC-MAEHARA", "M0652-L-MAEHARA", "source_map", "M0652-X-SOURCE"), ("PROV-ROOT", "M0652-X-PROVENANCE", "provenance_of", "M0652-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M0652-ROOT", "trusts", "M0652-S-FOUNDATION"), ("TRUST-RELEASE", "M0652-ROOT", "trusts", "M0652-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M0652-X-SOURCE", "documents", "M0652-ROOT"), ("DOC-BOUNDARY", "M0652-S-BOUNDARY", "documents", "M0652-N-CALCULUS")],
    "workflow": [("FLOW-PROOF", "M0652-T-ASSEMBLE", "workflow_depends_on", "M0652-T-SYNTACTIC"), ("FLOW-PROV", "M0652-X-PROVENANCE", "workflow_depends_on", "M0652-T-ASSEMBLE")],
}

def graph(raw):
    edges = raw if not raw or isinstance(raw[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in raw]
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof), **{name: graph(raw) for name, raw in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0652-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0652-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0652-S-DEFINITIONS", "M0652-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0652-B-COMPLETENESS", "M0652-T-SYNTACTIC", "M0652-B-SOUNDNESS"], "composition_certificates": ["Stage1Instances.THM_M_0652.statement_of_calculus_packages"], "reason": "Conditional composition elaborates, but all three substantive calculus packages remain premises."},
}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
