#!/usr/bin/env python3
"""Deterministically build the THM-M-1524 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1524-OBLIGATION_TREE"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1524-ROOT", "root", "critical", "Exact conjunction of Robertson and CCR-specialized uncertainty targets.", "Stage1Instances.THM_M_1524.HeisenbergUncertaintyTarget"),
    ("M1524-S-DEFINITIONS", "definition", "high", "Freeze observable application, expectation, deviation, commutator, and self-adjointness.", "Stage1Instances.THM_M_1524.Observable"),
    ("M1524-S-DOMAINS", "definition", "critical", "Retain density, state membership, and both product-domain witnesses.", "Stage1Instances.THM_M_1524.Observable.{domain,dense_domain,commutatorApply}"),
    ("M1524-S-BOUNDARY", "terminal", "normal", "Retain zero deviation, hbar = 0, and arbitrary complex Hilbert spaces.", "frozen Statement.lean binder and hypothesis boundary"),
    ("M1524-S-FOUNDATION", "certificate", "critical", "Audit transitive axioms, imports, TCB, and absence of oracle closure.", "planned transitive trust report"),
    ("M1524-N-CENTER", "normalization", "high", "Center A psi and B psi by their expectations and identify their norms with deviations.", "planned centered-vector identities"),
    ("M1524-L-SYMMETRY", "core_lemma", "critical", "Use symmetry on the explicit product domain to express the commutator expectation through centered inner products.", "planned commutator/imaginary-part identity"),
    ("M1524-L-CAUCHY-SCHWARZ", "core_lemma", "normal", "Bound the centered inner product norm by the product of centered norms.", "Stage1Instances.THM_M_1524.ObligationTree.centered_cauchy_schwarz"),
    ("M1524-L-ROBERTSON", "bridge", "critical", "Combine centering, symmetry, and Cauchy-Schwarz into the exact RobertsonTarget.", "Stage1Instances.THM_M_1524.RobertsonTarget"),
    ("M1524-L-CCR-SCALAR", "core_lemma", "high", "Rewrite the CCR commutator expectation and prove its norm equals hbar for a normalized state and nonnegative hbar.", "planned CCR scalar-norm identity"),
    ("M1524-T-CCR", "transport", "critical", "Specialize Robertson using the global CCR and scalar-norm identity.", "Stage1Instances.THM_M_1524.HeisenbergCCRTarget"),
    ("M1524-T-ASSEMBLE", "terminal", "high", "Pair exact Robertson and CCR child conclusions into the frozen conjunction.", "Stage1Instances.THM_M_1524.ObligationTree.exactTarget_of_components"),
    ("M1524-X-SOURCE", "terminal", "high", "Pinpoint Robertson/Heisenberg source assumptions and domain conventions.", "planned primary-source crosswalk"),
    ("M1524-X-PROVENANCE", "certificate", "critical", "Track terminal bodies, imports, revisions, axioms, validation, and replay.", "planned provenance closure"),
]

checked = {"M1524-S-DEFINITIONS", "M1524-S-DOMAINS", "M1524-S-BOUNDARY", "M1524-L-CAUCHY-SCHWARZ", "M1524-T-ASSEMBLE"}
source_na = {"M1524-S-DEFINITIONS", "M1524-S-DOMAINS", "M1524-S-BOUNDARY", "M1524-S-FOUNDATION", "M1524-X-PROVENANCE"}
machine_special = {"M1524-X-SOURCE": "not_applicable", "M1524-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:5acc7178fdf52c186852a6c6567826fee3b64f216541cb194d37fb6ea4211891"
obligations = []
nodes = []
for oid, kind, risk, claim, target in rows:
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": root_fp if oid == "M1524-ROOT" else "planned:v1:sha256:" + digest([oid, claim, target]),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1524/ObligationTree.lean#exactTarget_of_components" if oid == "M1524-T-ASSEMBLE" else ("mathlib:Mathlib.Analysis.InnerProductSpace.Basic#norm_inner_le_norm" if oid == "M1524-L-CAUCHY-SCHWARZ" else None),
    })
    premises = {
        "M1524-L-ROBERTSON": "Centered-vector identities, the symmetry identity, and Cauchy-Schwarz.",
        "M1524-T-CCR": "The exact Robertson conclusion, global CCR, normalization, and nonnegative hbar.",
        "M1524-T-ASSEMBLE": "Exact RobertsonTarget and exact HeisenbergCCRTarget child conclusions.",
    }.get(oid, "The frozen formal context and only the incoming typed proof requirements.")
    nodes.append({
        "node_id": "THM-M-1524-" + oid.removeprefix("M1524-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M2" if oid == "M1524-ROOT" else "M4"), "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit-provisional" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1524-T-ASSEMBLE" else ("pinned-mathlib-leaf" if oid == "M1524-L-CAUCHY-SCHWARZ" else "none"),
        "foundation_profile": "lean4-mathlib-classical/provisional", "tcb_profile": "lean-4.29.0+mathlib-8a178386/release-audit-pending",
        "computation_record": "none; no computation or oracle closes this node", "step_budget": 40,
        "semantic_step_ledger": {"premises": premises, "inference": claim, "output": claim, "outgoing_use": "Consumed only by the declared reciprocal composes edge, or recorded as a non-proof overlay."},
        "public_readable_target": "Stage1_Instances/THM-M-1524/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or checked conditional composition only; open analytic children receive no proof credit.",
        "task_ids": [ITEM, "S56-M-1524-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1524/ObligationTree.lean"] if oid in {"M1524-L-CAUCHY-SCHWARZ", "M1524-T-ASSEMBLE"} else [],
        "owner": "THM-M-1524 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1524", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and pre-status Robertson architecture; eligibility assigned independently of observed closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1524-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1524-X-PROVENANCE"]},
    "layer_applicability": {"statement": "expanded", "normalization": "centering required", "branch": "not_applicable: the proof has no mathematical case split; hbar nonnegativity handles the scalar norm uniformly", "construction": "centering construction represented by M1524-N-CENTER", "core_lemma": "expanded", "external": "expanded", "terminal": "expanded"},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M2"},
    "status_boundary": "Frozen denominator and conditional architecture only; symmetry, Robertson, CCR scalar evaluation, and the root remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1524-ROOT": ["M1524-T-ASSEMBLE"],
    "M1524-T-ASSEMBLE": ["M1524-L-ROBERTSON", "M1524-T-CCR"],
    "M1524-L-ROBERTSON": ["M1524-N-CENTER", "M1524-L-SYMMETRY", "M1524-L-CAUCHY-SCHWARZ"],
    "M1524-T-CCR": ["M1524-L-ROBERTSON", "M1524-L-CCR-SCALAR"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1524-ROOT", "logical_decomposition", "M1524-S-DEFINITIONS"), edge("REF-ROOT-DOMAINS", "M1524-ROOT", "logical_decomposition", "M1524-S-DOMAINS"), edge("REF-ROOT-BOUNDARY", "M1524-ROOT", "logical_decomposition", "M1524-S-BOUNDARY")],
    "provenance": [edge("SRC-ROBERTSON", "M1524-L-ROBERTSON", "source_map", "M1524-X-SOURCE"), edge("SRC-CCR", "M1524-T-CCR", "source_map", "M1524-X-SOURCE"), edge("PROV-ROOT", "M1524-X-PROVENANCE", "provenance_of", "M1524-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1524-ROOT", "trusts", "M1524-S-FOUNDATION"), edge("TRUST-PROV", "M1524-ROOT", "trusts", "M1524-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1524-S-DEFINITIONS", "documents", "M1524-ROOT"), edge("DOC-SOURCE", "M1524-X-SOURCE", "documents", "M1524-L-ROBERTSON")],
    "workflow": [edge("FLOW-ROB", "M1524-T-ASSEMBLE", "workflow_depends_on", "M1524-L-ROBERTSON"), edge("FLOW-CCR", "M1524-T-ASSEMBLE", "workflow_depends_on", "M1524-T-CCR"), edge("FLOW-PROV", "M1524-X-PROVENANCE", "workflow_depends_on", "M1524-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for value in edges:
        outgoing.setdefault(value["from"], []).append(value["edge_id"])
        incoming.setdefault(value["to"], []).append(value["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1524", "registry_id": "THM-M-1524-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1524-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1524-N-CENTER", "M1524-L-SYMMETRY", "M1524-L-CCR-SCALAR"], "composition_certificates": ["Stage1Instances.THM_M_1524.ObligationTree.exactTarget_of_components"], "reason": "The exact final composition is conditional on open Robertson and CCR analytic packages."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1524", "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1524/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations; denominator {denominator}")
