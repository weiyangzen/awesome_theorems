#!/usr/bin/env python3
"""Build the frozen THM-M-1143 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1143-OBLIGATION_TREE"
THEOREM = "THM-M-1143"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1143-ROOT", "root", "critical", "Exact bounded-harmonic-is-constant proposition in every positive finite dimension.", "Stage1Instances.THM_M_1143.BoundedHarmonicIsConstant", "The canonical proposition."),
    ("M1143-S-STATEMENT", "definition", "high", "Preserve positive dimension, global neighborhood harmonicity, two-sided bounded range, and pairwise constancy.", "Stage1Instances.THM_M_1143.BoundedHarmonicIsConstant", "The elaborated statement interface."),
    ("M1143-S-FOUNDATION", "certificate", "critical", "Freeze classical, choice, quotient, TCB, computation, and no-oracle boundaries.", "planned transitive axiom and TCB certificate", "Accepted trust boundary."),
    ("M1143-N-BOUND", "normalization", "high", "Extract a uniform absolute-value bound from bornological boundedness of the real range.", "planned IsBounded-range to norm-bound lemma", "A constant C bounding |f z| for all z."),
    ("M1143-L-GRADIENT", "core_lemma", "critical", "Prove the dimension-dependent interior gradient estimate on every ball centered at an arbitrary point.", "planned n-dimensional harmonic gradient estimate", "For each radius R, a bound on the derivative at the center proportional to C / R."),
    ("M1143-L-LIMIT", "lemma", "high", "Let the arbitrary ball radius tend to infinity in the gradient estimate.", "planned ordered-field limit argument", "The Frechet derivative vanishes at every point."),
    ("M1143-T-VANISH", "terminal", "critical", "Assemble boundedness, global harmonicity, the gradient estimate, and the radius limit.", "Stage1Instances.THM_M_1143.VanishingDerivativePackage", "A zero derivative at every point."),
    ("M1143-L-CONSTANT", "core_lemma", "high", "Deduce pairwise equality on the connected Euclidean space from a zero derivative everywhere.", "Stage1Instances.THM_M_1143.ZeroDerivativeConstantPackage", "The function is constant."),
    ("M1143-T-ASSEMBLE", "transport", "high", "Compose the derivative-vanishing and zero-derivative constancy packages into the exact target.", "Stage1Instances.THM_M_1143.root_of_vanishingDerivative_packages", "The canonical root, conditional on both packages."),
    ("M1143-X-PLANE", "anchor", "medium", "Track the pinned complex-plane harmonic Liouville theorem without generalizing its domain.", "InnerProductSpace.bounded_harmonic_on_complex_plane_is_constant", "A plane-only anchor and its terminal provenance."),
    ("M1143-X-SOURCE", "source_boundary", "high", "Map every analytic step to primary theorem/page, assumptions, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage only."),
    ("M1143-X-PROVENANCE", "certificate", "critical", "Inventory wrappers, terminal bodies, imports, axioms, TCB, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

checked = {"M1143-S-STATEMENT", "M1143-T-ASSEMBLE", "M1143-X-PLANE"}
source_na = {"M1143-S-STATEMENT", "M1143-S-FOUNDATION", "M1143-X-PROVENANCE"}
machine_modes = {"M1143-X-SOURCE": "not_applicable", "M1143-X-PROVENANCE": "informational", "M1143-X-PLANE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = "lean-expression-sha256:e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610" if oid in {"M1143-ROOT", "M1143-S-STATEMENT"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_modes.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "overlay_no_root_proof_credit"}.get(machine)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": oid != "M1143-X-PLANE", "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1143/ObligationTree.lean#root_of_vanishingDerivative_packages" if oid == "M1143-T-ASSEMBLE" else ("mathlib:Mathlib.Analysis.Complex.Harmonic.Liouville#bounded_harmonic_on_complex_plane_is_constant" if oid == "M1143-X-PLANE" else None),
    })
    nodes.append({
        "node_id": "THM-M-1143-" + oid.removeprefix("M1143-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H4", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1143-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "pinned-mathlib-plane-anchor" if oid == "M1143-X-PLANE" else ("local-conditional-composition" if oid == "M1143-T-ASSEMBLE" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle may close this node",
        "step_budget": 100 if oid == "M1143-L-GRADIENT" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the formal context.", "inference": claim, "output": output, "outgoing_use": "Only typed parent or support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1143/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise or root closure.",
        "task_ids": [ITEM, "S56-M-1143-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1143/ObligationTree.lean"] if oid == "M1143-T-ASSEMBLE" else [],
        "owner": "THM-M-1143 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: o[k] for k in fields} for o in obligations])
ids = [o["obligation_id"] for o in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact all-positive-dimensions statement, immutable anchor audit, and the classical gradient-estimate architecture; eligibility was assigned without treating the plane anchor as closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1143-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1143-X-PLANE", "M1143-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; the gradient estimate and derivative-to-constant packages remain open, so no root, audit, or theorem completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1143-ROOT": ["M1143-T-ASSEMBLE"],
    "M1143-T-ASSEMBLE": ["M1143-T-VANISH", "M1143-L-CONSTANT"],
    "M1143-T-VANISH": ["M1143-N-BOUND", "M1143-L-GRADIENT", "M1143-L-LIMIT"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

edge_groups = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-STATEMENT", "M1143-ROOT", "logical_decomposition", "M1143-S-STATEMENT"), edge("REF-ROOT-FOUNDATION", "M1143-ROOT", "logical_decomposition", "M1143-S-FOUNDATION")],
    "provenance": [edge("PROV-PLANE", "M1143-X-PLANE", "provenance_of", "M1143-L-GRADIENT"), edge("PROV-ROOT", "M1143-X-PROVENANCE", "provenance_of", "M1143-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M1143-ROOT", "trusts", "M1143-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M1143-ROOT", "trusts", "M1143-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M1143-S-STATEMENT", "documents", "M1143-ROOT"), edge("DOC-ANALYTIC", "M1143-X-SOURCE", "documents", "M1143-L-GRADIENT")],
    "workflow": [edge("FLOW-ASSEMBLE-VANISH", "M1143-T-ASSEMBLE", "workflow_depends_on", "M1143-T-VANISH"), edge("FLOW-ASSEMBLE-CONSTANT", "M1143-T-ASSEMBLE", "workflow_depends_on", "M1143-L-CONSTANT"), edge("FLOW-VANISH-GRADIENT", "M1143-T-VANISH", "workflow_depends_on", "M1143-L-GRADIENT"), edge("FLOW-PROVENANCE-ASSEMBLE", "M1143-X-PROVENANCE", "workflow_depends_on", "M1143-T-ASSEMBLE")],
}
graphs = {}
for name, edges in edge_groups.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1143-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1143-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1143-T-VANISH", "M1143-L-CONSTANT"], "composition_certificates": ["Stage1Instances.THM_M_1143.root_of_vanishingDerivative_packages"], "reason": "The checked final composition is conditional; both package parameters remain explicit and unproved."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1143/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
