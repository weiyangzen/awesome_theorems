#!/usr/bin/env python3
"""Deterministically build the THM-M-0645 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0645-OBLIGATION_TREE"
THEOREM = "THM-M-0645"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("M0645-ROOT", "root", "critical", "For every language and sentence, validity in every nonempty structure implies an empty-context derivation in the frozen calculus.", "Stage1Instances.THM_M_0645.CompletenessTarget", "The exact canonical completeness proposition."),
    ("M0645-D-CALCULUS", "definition", "high", "Preserve the finite classical natural-deduction rules, equality rules, Empty free-variable domain, and empty context fixed in Statement.lean.", "Stage1Instances.THM_M_0645.Derivation", "The exact syntactic derivability relation consumed at the root."),
    ("M0645-D-SEMANTICS", "definition", "high", "Preserve mathlib sentence realization over every nonempty structure of arbitrary universe-polymorphic language.", "Stage1Instances.THM_M_0645.Valid", "The exact semantic validity premise consumed at the root."),
    ("M0645-R-NEG-CONSISTENT", "reduction", "critical", "Reduce validity of phi to syntactic consistency of the empty theory extended by not phi, using the frozen classical calculus.", "planned signature: Valid phi -> Consistent ([phi.not])", "Consistency input for the Henkin extension, with the derivability notion fixed."),
    ("M0645-C-HENKIN", "construction", "critical", "Extend a consistent theory to a complete witness-saturated Henkin theory while preserving consistency.", "planned signature: Consistent T -> exists H, HenkinCompleteExtension T H", "A complete consistent extension with witnesses for existential formulas."),
    ("M0645-C-TERM-MODEL", "construction", "critical", "Construct the canonical term model, quotienting closed terms by provable equality and proving language operations well-defined.", "planned signature: HenkinCompleteExtension T H -> TermModel H", "A nonempty structure for the original language with equality respected."),
    ("M0645-L-EQUALITY", "core_lemma", "critical", "Show provable equality is an equivalence and a congruence for every function and relation symbol.", "planned equality congruence package for Derivation", "Well-defined quotient operations and equality semantics in the term model."),
    ("M0645-L-TRUTH", "core_lemma", "critical", "Prove by formula induction that term-model realization agrees with membership in the complete Henkin theory.", "planned truth lemma for every formula and valuation", "The term model satisfies exactly the formulas selected by the Henkin theory."),
    ("M0645-R-COUNTERMODEL", "reduction", "critical", "From a derivation failure for phi, assemble the Henkin term model and use the truth lemma to obtain a nonempty countermodel to phi.", "planned signature: Not (Provable phi) -> exists M, Nonempty M and not (M models phi)", "Contrapositive completeness for the exact semantic and syntactic interfaces."),
    ("M0645-T-CLASSICAL", "transport", "high", "Apply classical contraposition and eliminate double negation to turn the countermodel construction into Valid phi -> Provable phi.", "planned classical transport", "CompletenessDerivationBuilder for all languages and sentences."),
    ("M0645-T-ASSEMBLE", "terminal", "high", "Consume CompletenessDerivationBuilder and introduce the exact ordered root binders.", "Stage1Instances.THM_M_0645.completenessTarget_of_builder", "The exact CompletenessTarget, conditional on the substantive builder."),
    ("M0645-X-EXTERNAL", "bridge", "critical", "Translate Foundation's language, proof calculus, equality assumptions, and semantic consequence into the frozen mathlib-based target before any imported body can receive credit.", "planned checked external transport; currently unavailable", "An optional exact external integration route, without current proof credit."),
    ("M0645-X-SOURCE", "terminal", "high", "Map each reduction, Henkin construction, term model, equality argument, and truth lemma to pinpoint primary-source passages and errata.", "non-machine primary-source node map", "Human-source coverage separate from machine proof status."),
    ("M0645-X-PROVENANCE", "certificate", "critical", "Bind every wrapper and imported conclusion to its unique terminal body, immutable revision, dependency closure, and license.", "planned provenance packet", "Deduplicated proof-body provenance without semantic proof credit."),
    ("M0645-X-TRUST", "certificate", "critical", "Audit transitive imports, axioms, placeholders, unsafe paths, generated artifacts, kernel, and the no-oracle boundary.", "planned trust report", "Accepted TCB and foundation boundary for later release."),
]

source_na = {"M0645-D-CALCULUS", "M0645-D-SEMANTICS", "M0645-X-PROVENANCE", "M0645-X-TRUST"}
machine_overlay = {"M0645-X-SOURCE": "not_applicable", "M0645-X-PROVENANCE": "informational", "M0645-X-TRUST": "informational"}
conditional = {"M0645-T-ASSEMBLE"}
statement_hash = hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = "lean-expression-sha256:76fbce831cb0d1669af8754a6c4f3c3d45d0e4fbbab1532e0140104937c7ea68" if oid == "M0645-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_overlay.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "assurance_overlay_no_semantic_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-0645/ObligationTree.lean#completenessTarget_of_builder" if oid == "M0645-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": "THM-M-0645-" + oid.removeprefix("M0645-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in conditional else ("M3" if oid in {"M0645-ROOT", "M0645-D-CALCULUS", "M0645-D-SEMANTICS"} else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if body else ("foundation-anchor-transport-pending" if oid == "M0645-X-EXTERNAL" else "none"),
        "foundation_profile": "lean4-mathlib classical calculus/final policy audit pending", "tcb_profile": "Lean-4.29.0+mathlib-8a178386/transitive closure pending",
        "computation_record": "none; no evaluator, certificate, external code, or oracle receives proof credit",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only outputs arriving on declared proof_requires edges in the frozen context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0645/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no unlisted premise, root closure, or theorem completion.",
        "task_ids": [ITEM, "S56-M-0645-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0645/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0645 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in conditional else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement.json", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid in conditional else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact elaborated target, audited no-local-anchor result, and the standard Henkin/term-model architecture; eligibility frozen independently of closure status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0645-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0645-X-PROVENANCE", "M0645-X-TRUST"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"conditionally_checked_obligations": sorted(conditional), "accepted_root_machine_debt": "M4"},
    "status_boundary": "Frozen architecture only; no Henkin proof, external transport, accepted root closure, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0645-ROOT": ["M0645-T-ASSEMBLE", "M0645-D-CALCULUS", "M0645-D-SEMANTICS"],
    "M0645-T-ASSEMBLE": ["M0645-T-CLASSICAL"],
    "M0645-T-CLASSICAL": ["M0645-R-COUNTERMODEL"],
    "M0645-R-COUNTERMODEL": ["M0645-R-NEG-CONSISTENT", "M0645-C-HENKIN", "M0645-C-TERM-MODEL", "M0645-L-TRUTH"],
    "M0645-C-TERM-MODEL": ["M0645-L-EQUALITY"],
    "M0645-L-TRUTH": ["M0645-C-HENKIN", "M0645-C-TERM-MODEL"],
    "M0645-C-HENKIN": ["M0645-R-NEG-CONSISTENT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-CALCULUS", "M0645-ROOT", "logical_decomposition", "M0645-D-CALCULUS"), edge("REF-ROOT-SEMANTICS", "M0645-ROOT", "logical_decomposition", "M0645-D-SEMANTICS")],
    "provenance": [edge("SRC-HENKIN", "M0645-C-HENKIN", "source_map", "M0645-X-SOURCE"), edge("SRC-TRUTH", "M0645-L-TRUTH", "source_map", "M0645-X-SOURCE"), edge("PROV-EXTERNAL", "M0645-X-PROVENANCE", "provenance_of", "M0645-X-EXTERNAL"), edge("PROV-ASSEMBLE", "M0645-X-PROVENANCE", "provenance_of", "M0645-T-ASSEMBLE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0645-ROOT", "trusts", "M0645-X-TRUST"), edge("TRUST-EXTERNAL", "M0645-X-EXTERNAL", "trusts", "M0645-X-TRUST")],
    "documentation": [edge("DOC-SOURCE", "M0645-X-SOURCE", "documents", "M0645-ROOT"), edge("DOC-PROVENANCE", "M0645-X-PROVENANCE", "documents", "M0645-X-EXTERNAL")],
    "workflow": [edge("FLOW-ASSEMBLE-CLASSICAL", "M0645-T-ASSEMBLE", "workflow_depends_on", "M0645-T-CLASSICAL"), edge("FLOW-CLASSICAL-COUNTER", "M0645-T-CLASSICAL", "workflow_depends_on", "M0645-R-COUNTERMODEL"), edge("FLOW-COUNTER-TRUTH", "M0645-R-COUNTERMODEL", "workflow_depends_on", "M0645-L-TRUTH"), edge("FLOW-TRUTH-MODEL", "M0645-L-TRUTH", "workflow_depends_on", "M0645-C-TERM-MODEL"), edge("FLOW-MODEL-HENKIN", "M0645-C-TERM-MODEL", "workflow_depends_on", "M0645-C-HENKIN"), edge("FLOW-HENKIN-CONSISTENT", "M0645-C-HENKIN", "workflow_depends_on", "M0645-R-NEG-CONSISTENT"), edge("FLOW-EXTERNAL-PROV", "M0645-X-EXTERNAL", "workflow_depends_on", "M0645-X-PROVENANCE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0645-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator, "root_node_id": "M0645-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"conditionally_checked_obligations": sorted(conditional), "accepted_root_closed": False, "accepted_root_machine_debt": "M4", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0645-T-CLASSICAL"], "composition_certificates": ["Stage1Instances.THM_M_0645.completenessTarget_of_builder"], "reason": "Final binder assembly is checked, but every substantive Henkin/term-model package is open and the external anchor lacks a checked transport."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0645/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0645 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THM_M_0645.completenessTarget_of_builder"] if oid == "M0645-T-ASSEMBLE" else []} for oid, *_ in rows]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
