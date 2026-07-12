#!/usr/bin/env python3
"""Build the frozen THM-M-0644 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0644-OBLIGATION_TREE"
THEOREM = "THM-M-0644"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0644-ROOT", "root", "critical", "Every first-order theory is satisfiable iff every finite subtheory is satisfiable.", "forall {L : FirstOrder.Language.{u,v}} {T : L.Theory}, T.IsSatisfiable iff T.IsFinitelySatisfiable", "The exact canonical compactness proposition."),
    ("M0644-S-DEFINITIONS", "definition", "high", "Freeze nonempty model satisfiability, Finset subtheories, containment, universes, and the finite-Set transport.", "Stage1.THM_M_0644.{CompactnessTarget,FinsetExpandedTarget,FiniteSetTarget}", "The exact elaborated statement interface."),
    ("M0644-S-BOUNDARY", "terminal", "normal", "Include empty languages, empty theories, and the empty finite subtheory without countability assumptions.", "boundary cases implicit in CompactnessTarget", "All degenerate cases retain the canonical quantifiers."),
    ("M0644-S-FOUNDATION", "certificate", "critical", "Freeze classical choice, propositional extensionality, quotient soundness, kernel, and no-oracle policy.", "planned transitive axiom and TCB report", "An accepted trust boundary."),
    ("M0644-B-FORWARD", "branch", "normal", "Restrict any model of T along each finite-subtheory inclusion.", "Stage1.THM_M_0644.ObligationTree.RestrictionDirection", "T.IsSatisfiable implies T.IsFinitelySatisfiable."),
    ("M0644-L-MONO", "core_lemma", "normal", "Use satisfiability monotonicity for theory inclusion.", "FirstOrder.Language.Theory.IsSatisfiable.mono", "Each included finite theory inherits a model."),
    ("M0644-B-BACKWARD", "branch", "critical", "Construct a model of T from models of all finite subtheories by the ultraproduct argument.", "Stage1.THM_M_0644.ObligationTree.UltraproductDirection", "T.IsFinitelySatisfiable implies T.IsSatisfiable."),
    ("M0644-C-FINITE-MODELS", "construction", "high", "Choose a carrier model for every finite subtheory of T.", "mathlib body: M : Finset T -> Type (max u v)", "A family of nonempty structures satisfying their indexed finite theories."),
    ("M0644-C-ULTRAFILTER", "construction", "critical", "Put the ultrafilter extending atTop on the directed set Finset T over the finite-model family.", "Ultrafilter.of (Filter.atTop : Filter (Finset T))", "An ultrafilter containing every tail of finite subtheories."),
    ("M0644-C-ULTRAPRODUCT", "construction", "critical", "Form the filter product of the finite-model carriers and induced language structures.", "Filter.Product (Ultrafilter.of (Filter.atTop : Filter (Finset T))) M", "The candidate ultraproduct model M'."),
    ("M0644-L-EVENTUAL", "core_lemma", "critical", "For each sentence phi in T, show that all finite subtheories above {phi} realize phi.", "Filter.Eventually.filter_mono plus Filter.eventually_atTop", "The set of component models realizing phi belongs to the ultrafilter."),
    ("M0644-L-LOS", "bridge", "critical", "Transport eventual component realization to realization in the filter product.", "FirstOrder.Language.Ultraproduct.sentence_realize", "M' realizes every sentence of T."),
    ("M0644-T-MODEL", "terminal", "high", "Package the ultraproduct structure satisfying T as Theory.IsSatisfiable.", "ModelType.of T M'", "T.IsSatisfiable."),
    ("M0644-T-ASSEMBLE", "transport", "high", "Combine restriction and ultraproduct directions into the exact iff target.", "Stage1.THM_M_0644.ObligationTree.root_of_directions", "The exact canonical root conditional on both directions."),
    ("M0644-X-SOURCE", "terminal", "high", "Map each material proof node to a reviewed primary mathematical source passage.", "non-machine node-specific source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0644-X-PROVENANCE", "certificate", "critical", "Inventory the selected terminal body, imports, axioms, wrappers, hashes, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without duplicate proof credit."),
]

checked = {"M0644-S-DEFINITIONS", "M0644-T-ASSEMBLE"}
source_na = {"M0644-S-DEFINITIONS", "M0644-S-BOUNDARY", "M0644-S-FOUNDATION", "M0644-X-PROVENANCE"}
machine_special = {"M0644-X-SOURCE": "not_applicable", "M0644-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M0644-ROOT", "M0644-S-DEFINITIONS"} else ("planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    body = "local:Stage1_Instances/THM-M-0644/ObligationTree.lean#root_of_directions" if oid == "M0644-T-ASSEMBLE" else ("mathlib:Mathlib.ModelTheory.Satisfiability#isSatisfiable_iff_isFinitelySatisfiable" if oid == "M0644-ROOT" else None)
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    obligations.append({"obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": "THM-M-0644-" + oid.removeprefix("M0644-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output, "human_debt": "H1",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0644-ROOT" else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0644-T-ASSEMBLE" else ("pinned-mathlib-body-audit-pending" if oid not in source_na else "none"),
        "foundation_profile": "lean4-mathlib-classical/propext-choice-quotient", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no solver, oracle, or external computation may close this node", "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0644/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; accepted root closure and release assurance are not supplied.",
        "task_ids": [ITEM, "S56-M-0644-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0644/ObligationTree.lean"] if oid == "M0644-T-ASSEMBLE" else [],
        "owner": "THM-M-0644 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and bounded anchor audit; the selected pinned ultraproduct body's semantic architecture was expanded before recording closure status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M0644-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0644-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen denominator only; anchor availability is not accepted proof, source, provenance, audit, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0644-ROOT": ["M0644-T-ASSEMBLE"], "M0644-T-ASSEMBLE": ["M0644-B-FORWARD", "M0644-B-BACKWARD"],
    "M0644-B-FORWARD": ["M0644-L-MONO"], "M0644-B-BACKWARD": ["M0644-C-FINITE-MODELS", "M0644-C-ULTRAFILTER", "M0644-C-ULTRAPRODUCT", "M0644-L-EVENTUAL", "M0644-L-LOS", "M0644-T-MODEL"],
    "M0644-C-ULTRAPRODUCT": ["M0644-C-FINITE-MODELS", "M0644-C-ULTRAFILTER"], "M0644-L-EVENTUAL": ["M0644-C-FINITE-MODELS", "M0644-C-ULTRAFILTER"],
    "M0644-T-MODEL": ["M0644-C-ULTRAPRODUCT", "M0644-L-EVENTUAL", "M0644-L-LOS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0644-ROOT", "logical_decomposition", "M0644-S-DEFINITIONS"), edge("REF-ROOT-BOUNDARY", "M0644-ROOT", "logical_decomposition", "M0644-S-BOUNDARY")],
    "provenance": [edge("SRC-BACKWARD", "M0644-B-BACKWARD", "source_map", "M0644-X-SOURCE"), edge("PROV-ROOT", "M0644-X-PROVENANCE", "provenance_of", "M0644-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0644-ROOT", "trusts", "M0644-S-FOUNDATION"), edge("TRUST-PROV", "M0644-ROOT", "trusts", "M0644-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0644-S-DEFINITIONS", "documents", "M0644-ROOT"), edge("DOC-SOURCE", "M0644-X-SOURCE", "documents", "M0644-B-BACKWARD")],
    "workflow": [edge("FLOW-ASSEMBLE-FORWARD", "M0644-T-ASSEMBLE", "workflow_depends_on", "M0644-B-FORWARD"), edge("FLOW-ASSEMBLE-BACKWARD", "M0644-T-ASSEMBLE", "workflow_depends_on", "M0644-B-BACKWARD"), edge("FLOW-PROV-ASSEMBLE", "M0644-X-PROVENANCE", "workflow_depends_on", "M0644-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0644-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0644-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0644-B-FORWARD", "M0644-B-BACKWARD"], "composition_certificates": ["Stage1.THM_M_0644.ObligationTree.root_of_directions"], "reason": "The composition is conditional and accepted proof/provenance receipts are deferred to later phases."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in ids:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0644/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0644 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(x) for x in graph_edges.values())} typed edges")
print(denominator)
