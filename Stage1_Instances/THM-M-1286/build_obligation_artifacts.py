#!/usr/bin/env python3
"""Generate the frozen THM-M-1286 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1286-OBLIGATION_TREE"
THEOREM = "THM-M-1286"
PREFIX = "M1286"

ROWS = [
    ("ROOT", "root", "Exact finite-p whole-space Polya-Szego target.", "Stage1Instances.THM_M_1286.PolyaSzegoTarget", "critical", "required", "required", "required"),
    ("S-EXACT", "definition", "Definitions and binder order coincide with the frozen expanded target.", "PolyaSzegoTarget ↔ ExpandedTarget", "high", "required", "not_applicable", "required"),
    ("S-BOUNDARY", "terminal", "Dimension, exponent, nonnegativity, and finite-superlevel boundaries are retained.", "1 ≤ n ∧ 1 ≤ p ∧ p ≠ ∞ with the frozen input hypotheses", "high", "required", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit classical choice, measure theory, Bochner integration, and weak derivatives.", "Exact declaration dependency and trust report", "critical", "required", "not_applicable", "required"),
    ("N-REGIME", "normalization", "Reduce only within the fixed nonnegative finite-p whole-space regime.", "Normalized input preserving every frozen hypothesis", "high", "required", "required", "required"),
    ("C-REARRANGE", "construction", "Construct the Schwarz symmetric decreasing rearrangement.", "RearrangementConstruction", "critical", "required", "required", "required"),
    ("C-DISTRIBUTION", "definition", "Build the distribution function from positive superlevel measures.", "Canonical antitone distribution function of u", "high", "required", "required", "required"),
    ("C-RADIUS", "construction", "Convert distribution values to centered-ball radii and define uStar.", "Measurable radial-antitone uStar", "critical", "required", "required", "required"),
    ("C-EQUIMEAS", "core_lemma", "Prove measurability, MemLp preservation, symmetry, and equimeasurability.", "All four conclusions of RearrangementConstruction", "critical", "required", "required", "required"),
    ("L-GRADIENT", "bridge", "Produce a weak gradient of uStar and prove its p-energy bound.", "GradientEstimate", "critical", "required", "required", "required"),
    ("L-SMOOTH", "core_lemma", "Prove the rearrangement gradient inequality for smooth approximants.", "Smooth finite-p Polya-Szego estimate", "critical", "required", "required", "required"),
    ("L-COAREA", "core_lemma", "Relate gradient energy to perimeters of level sets.", "Coarea/layer-cake energy identity or inequality", "critical", "required", "required", "required"),
    ("L-ISOPERIMETRIC", "core_lemma", "Compare each level set with the equimeasurable centered ball.", "Perimeter lower bound at almost every level", "critical", "required", "required", "required"),
    ("L-APPROX", "construction", "Approximate Sobolev inputs while preserving the required convergence.", "Smooth approximation and rearrangement convergence package", "critical", "required", "required", "required"),
    ("L-LSC", "core_lemma", "Pass the gradient estimate to the weak limit.", "Weak-gradient existence and lower semicontinuity bound", "critical", "required", "required", "required"),
    ("T-ASSEMBLE", "terminal", "Compose construction and gradient packages into the exact root.", "exactTarget_of_packages", "high", "required", "required", "required"),
    ("X-SOURCE", "terminal", "Map all analytic premises to pinpoint primary-source arguments.", "Reviewed source crosswalk", "high", "not_applicable", "required", "required"),
    ("X-PROVENANCE", "certificate", "Track terminal bodies, imports, trust, and evidence without proof credit.", "Release provenance overlay", "critical", "informational", "not_applicable", "required"),
]

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()

def oid(short):
    return f"{PREFIX}-{short}"

def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": oid(source), "type": kind, "to": oid(target)}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row

obligations = []
nodes = []
for short, kind, statement, formal, risk, machine, human, readable in ROWS:
    obligation = oid(short)
    fingerprint = ("lean-expression-sha256:" if short == "ROOT" else "planned:v1:sha256:") + digest(formal)
    exclusion = None
    if machine == "not_applicable": exclusion = "human_source_boundary_only"
    if machine == "informational": exclusion = "release_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": obligation, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1286/ObligationTree.lean#exactTarget_of_packages" if short == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{short}", "obligation_id": obligation, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": statement,
        "human_debt": "H3", "machine_debt": "M4", "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit:open-source-pinpoint" if human == "required" else "not-applicable",
        "provenance_id": "local:ObligationTree.lean" if short in ("C-REARRANGE", "L-GRADIENT", "T-ASSEMBLE") else "none",
        "foundation_profile": "lean4-dependent-type-theory/review-pending",
        "tcb_profile": "lean-4.29.0/transitive-audit-pending", "computation_record": "none",
        "step_budget": 12 if kind not in ("root", "construction", "bridge") else 24,
        "semantic_step_ledger": {"premises": "Named incoming typed edges", "inference": statement, "output": statement, "outgoing_use": "Named outgoing typed edges"},
        "public_readable_target": f"Stage1_Instances/THM-M-1286/obligation-tree.md#{obligation.lower()}",
        "validation_spec_id": f"VAL-{obligation}",
        "status_boundary": "Architecture only; no open analytic premise or theorem closure is claimed.",
        "task_ids": [ITEM, "S56-M-1286-PROOF"], "owned_sources": [],
        "owner": "THM-M-1286 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,source,toolchain change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = digest(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact frozen statement and pre-closure Polya-Szego architecture; eligibility assigned independently of available proof bodies.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [oid("X-PROVENANCE")],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [oid("S-EXACT"), oid("T-ASSEMBLE")], "root_machine_debt": "M4"},
    "status_boundary": "Frozen denominator and conditional architecture only; construction and analytic estimates remain open.",
}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "C-REARRANGE"), ("T-ASSEMBLE", "L-GRADIENT")]
proof = []
for parent, child in proof_pairs:
    fwd, rev = f"PR-{parent}-{child}", f"CO-{child}-{parent}"
    proof.extend([edge(fwd, parent, "proof_requires", child, rev), edge(rev, child, "composes", parent, fwd)])
refinement_pairs = [
    ("ROOT", "S-EXACT"), ("ROOT", "S-BOUNDARY"), ("ROOT", "S-FOUNDATION"), ("ROOT", "N-REGIME"),
    ("C-REARRANGE", "C-DISTRIBUTION"), ("C-REARRANGE", "C-RADIUS"), ("C-REARRANGE", "C-EQUIMEAS"),
    ("L-GRADIENT", "L-SMOOTH"), ("L-GRADIENT", "L-COAREA"), ("L-GRADIENT", "L-ISOPERIMETRIC"),
    ("L-GRADIENT", "L-APPROX"), ("L-GRADIENT", "L-LSC"),
]

graphs_raw = {
    "proof": proof,
    "refinement": [edge(f"LD-{a}-{b}", a, "logical_decomposition", b) for a,b in refinement_pairs],
    "provenance": [edge("PV-ASSEMBLE", "T-ASSEMBLE", "provenance_of", "X-PROVENANCE")],
    "source": [edge("SM-ROOT-SOURCE", "ROOT", "source_map", "X-SOURCE")],
    "trust": [edge("TR-ROOT-FOUNDATION", "ROOT", "trusts", "S-FOUNDATION")],
    "documentation": [edge("DO-ROOT-SOURCE", "ROOT", "documents", "X-SOURCE")],
    "workflow": [edge("WF-SOURCE-PROOF", "X-SOURCE", "workflow_depends_on", "T-ASSEMBLE")],
}
graphs = {}
for name, edges in graphs_raw.items():
    outgoing, incoming = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [oid("S-EXACT"), oid("T-ASSEMBLE")], "root_closed": False,
        "root_machine_debt": "M4", "remaining_root_cut_set": [oid("C-REARRANGE"), oid("L-GRADIENT")],
        "composition_certificates_checked": ["exactTarget_of_packages"], "theorem_complete": False,
    },
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
           "recipes": [{"recipe_id": f"VAL-{row['obligation_id']}", "status": "open", "command": "future node-scoped Lean validation"} for row in obligations]}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps(recipes, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in graphs_raw.values())} typed edges")
