#!/usr/bin/env python3
"""Build the frozen THM-M-0996 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "M0996"


def digest(value):
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


specs = [
    ("ROOT", "root", "The exact finite-dimensional standard-Gaussian half-space enlargement comparison.", "Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget", "The frozen root proposition.", "critical", "split-required"),
    ("S-EXACT", "definition", "Freeze standard Gaussian measure, open thickening, measurable set, unit-normal half-space, and positive radius.", "Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget", "An exact statement context for every proof child.", "high", 8),
    ("S-BOUNDARY", "branch", "Account for positive radius, zero dimension, and null or full Gaussian measure without an inverse-CDF endpoint convention.", "The binders and conventions recorded in statement.json", "The complete boundary policy consumed by the proof route.", "high", 10),
    ("S-TRANSPORT", "transport", "Identify the expanded statement shape with the canonical target.", "Stage1Instances.THM_M_0996.target_iff_expandedStatementShape", "A checked iff transport to the exact root.", "normal", 1),
    ("S-FOUNDATION", "certificate", "Audit classical choice, quotient, extensionality, measure theory, and all transitive axioms.", "Axiom/foundation certificate for the eventual root body", "The accepted logical boundary.", "critical", 12),
    ("N-PROFILE", "normalization", "Choose and freeze a Gaussian enlargement profile whose argument is the Gaussian mass, including endpoint behavior.", "planned: profile : ENNReal -> Real -> ENNReal", "A common comparison quantity for the arbitrary set and its equal-measure half-space.", "critical", "split-required"),
    ("N-COORD", "normalization", "Transport finite-dimensional standard Gaussian space through an orthonormal coordinate equivalence without changing distances or measure.", "ProbabilityTheory.stdGaussian_eq_map_pi_orthonormalBasis plus metric compatibility", "A Euclidean-coordinate form of the target.", "high", 30),
    ("B-DIM", "branch", "Separate the vacuous zero-dimensional unit-halfspace case and the positive-dimensional analytic case, then recompose.", "FiniteDimensional.finrank Real E = 0 or 0 < FiniteDimensional.finrank Real E", "An exhaustive dimension branch.", "high", 18),
    ("C-HALFSPACE", "construction", "Represent every unit-normal affine half-space in coordinates and identify its metric thickening.", "IsUnitHalfspace H -> coordinate halfspace and thickening identity", "A one-dimensional threshold representation for H and its enlargement.", "critical", "split-required"),
    ("C-SEMIGROUP", "construction", "Construct the finite-dimensional Ornstein-Uhlenbeck interpolation used by the analytic comparison.", "planned: Ornstein-Uhlenbeck semigroup on standard Gaussian space", "A measure-preserving interpolation with the required regularity.", "critical", "split-required"),
    ("L-HALFSPACE", "core_lemma", "Compute the Gaussian measure of a unit half-space and all positive open thickenings in the frozen profile.", "HalfspaceEnlargementFormula profile", "stdGaussian E (thickening r H) = profile (stdGaussian E H) r.", "critical", "split-required"),
    ("L-GRADIENT", "core_lemma", "Establish the semigroup gradient and regularity estimates required by Gaussian comparison.", "planned: gradient estimate for the Ornstein-Uhlenbeck interpolation", "The differential inequality input for interpolation.", "critical", "split-required"),
    ("L-INTERPOLATE", "core_lemma", "Integrate the Gaussian comparison differential inequality from the smoothed set indicator to the profile bound.", "planned: semigroup interpolation comparison", "The profile inequality for regularized indicators.", "critical", "split-required"),
    ("L-LIMIT", "core_lemma", "Pass from regularized or approximating sets to every measurable set while preserving the open-thickening inequality.", "planned: measurable approximation and limiting theorem", "The arbitrary measurable-set profile lower bound.", "critical", "split-required"),
    ("L-GENERAL", "core_lemma", "Prove the profile lower bound for every measurable set and positive radius.", "GeneralSetEnlargementBound profile", "profile (stdGaussian E A) r <= stdGaussian E (thickening r A).", "critical", "split-required"),
    ("T-ASSEMBLE", "terminal", "Rewrite the half-space measure by its profile, use equal initial measures, and apply the arbitrary-set bound.", "Stage1Instances.THM_M_0996.target_of_profile_bounds", "The exact canonical target conditional on L-HALFSPACE and L-GENERAL.", "critical", 5),
    ("X-ANCHORS", "certificate", "Track the pinned mathlib Gaussian, coordinate, real-measure, and thickening anchors without assigning root proof credit.", "anchor-audit.json candidate inventory", "Pinned dependency provenance only.", "high", 12),
    ("X-SOURCE", "certificate", "Map every root-critical analytic step to pinpoint primary-source theorem, assumptions, and errata.", "non-machine source crosswalk", "Reviewed H evidence with no machine proof credit.", "critical", "split-required"),
    ("X-TCB", "certificate", "Record terminal proof bodies, transitive imports, toolchain, foundation policy, and reproducibility inputs.", "trust/provenance closure certificate", "A release-gate trust record with no proof credit.", "critical", 20),
]

machine_ids = [f"{PREFIX}-{s[0]}" for s in specs if not s[0].startswith("X-")]
source_ids = [f"{PREFIX}-{s[0]}" for s in specs if s[0] not in {"S-TRANSPORT", "S-FOUNDATION", "X-ANCHORS", "X-TCB"}]
all_ids = [f"{PREFIX}-{s[0]}" for s in specs]
denominators = {
    "inventory": all_ids,
    "required_machine": machine_ids,
    "required_human_source": source_ids,
    "required_readable": all_ids,
    "informational_overlays": [f"{PREFIX}-X-ANCHORS", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-TCB"],
}
denominator_sha = digest(denominators)

obligations = []
nodes = []
for suffix, kind, statement, formal, output, risk, budget in specs:
    oid = f"{PREFIX}-{suffix}"
    overlay = suffix.startswith("X-")
    fingerprint = (
        "lean-source-sha256:cdecb06daf3ca5cbc2b6f8f5def0a82fb3fc712695fdd5c2a047189d683edd14"
        if suffix in {"ROOT", "S-EXACT"}
        else "planned:v1:sha256:" + digest({"id": oid, "formal_target": formal})
    )
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": not overlay, "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "required" if oid in source_ids else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "assurance_overlay_no_proof_credit" if overlay else None,
        "terminal_proof_body_id": "local:Stage1Instances.THM_M_0996.target_of_profile_bounds" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"THM-M-0996-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M3" if suffix in {"ROOT", "S-EXACT", "S-TRANSPORT", "T-ASSEMBLE"} else "M4",
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-audit-pending" if oid in source_ids else "not-applicable",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("pinned-anchor-inventory" if suffix == "X-ANCHORS" else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or numerical experiment may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "The exact context and only the incoming typed proof/refinement obligations.",
            "inference": statement, "output": output,
            "source_anchors": "pending pinpoint source audit" if oid in source_ids else "not-applicable",
            "outgoing_use": "Only declared typed edges may consume this output."
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0996/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING",
        "status_boundary": "Architecture or conditional composition only; this phase credits no Gaussian isoperimetric proof body or accepted closure.",
        "task_ids": ["S56-M-0996-OBLIGATION_TREE", "S56-M-0996-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0996/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-0996 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if suffix == "T-ASSEMBLE" else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"],
                     "revocation_state": "provisional" if suffix == "T-ASSEMBLE" else "open"},
    })

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0996-OBLIGATION_TREE",
    "theorem_id": "THM-M-0996", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and negative pinned anchor audit; Gaussian semigroup comparison architecture; eligibility assigned before proof-phase closure observation.",
    "frozen_against_statement_sha256": "bca25f50f58fa2d386905a6520ed390367dac4a029175d0eb66899b1ffe790f7",
    "frozen_against_anchor_audit_sha256": "37a8f757f327d13d6be0b260b2c70c53cddf30bca7ffd1e21bbb63cba8d282e5",
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator_sha,
    "frozen_denominators": denominators,
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [], "conditionally_checked_compositions": [f"{PREFIX}-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen architecture and conditional composition only; both central profile bounds and the root remain open."
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-HALFSPACE"), ("T-ASSEMBLE", "L-GENERAL"),
    ("L-HALFSPACE", "C-HALFSPACE"), ("L-HALFSPACE", "N-PROFILE"),
    ("L-GENERAL", "L-LIMIT"), ("L-LIMIT", "L-INTERPOLATE"),
    ("L-INTERPOLATE", "L-GRADIENT"), ("L-INTERPOLATE", "C-SEMIGROUP"),
    ("L-GENERAL", "N-PROFILE"), ("C-HALFSPACE", "N-COORD"),
]
proof_edges = []
for parent, child in proof_pairs:
    p, c = f"{PREFIX}-{parent}", f"{PREFIX}-{child}"
    req, comp = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": req, "from": p, "type": "proof_requires", "to": c, "reciprocal_edge_id": comp},
        {"edge_id": comp, "from": c, "type": "composes", "to": p, "reciprocal_edge_id": req},
    ])

refinement_pairs = [
    ("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-TRANSPORT"),
    ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-PROFILE"), ("ROOT", "N-COORD"),
    ("ROOT", "B-DIM"), ("B-DIM", "C-HALFSPACE"), ("B-DIM", "C-SEMIGROUP"),
]
refinement_edges = [{"edge_id": f"REFINE-{a}-{b}", "from": f"{PREFIX}-{a}", "type": "logical_decomposition", "to": f"{PREFIX}-{b}"} for a, b in refinement_pairs]

def edges(kind, pairs, edge_type):
    return [{"edge_id": f"{kind}-{i+1}", "from": f"{PREFIX}-{a}", "type": edge_type, "to": f"{PREFIX}-{b}"} for i, (a, b) in enumerate(pairs)]

graphs = {
    "proof": {"edges": proof_edges},
    "refinement": {"edges": refinement_edges},
    "provenance": {"edges": edges("PROV", [("S-EXACT", "X-ANCHORS"), ("N-COORD", "X-ANCHORS"), ("T-ASSEMBLE", "X-TCB")], "provenance_of")},
    "evidence": {"edges": edges("EVID", [("T-ASSEMBLE", "X-TCB")], "evidence_for")},
    "trust": {"edges": edges("TRUST", [("ROOT", "X-TCB"), ("T-ASSEMBLE", "X-TCB")], "trusts")},
    "documentation": {"edges": edges("DOC", [(s[0], "X-SOURCE") for s in specs if f"{PREFIX}-{s[0]}" in source_ids], "documents")},
    "workflow": {"edges": [{"edge_id": "WORKFLOW-OBLIGATION-PROOF", "from": "S56-M-0996-OBLIGATION_TREE", "type": "workflow_depends_on", "to": "S56-M-0996-PROOF"}]},
}

typed = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0996-OBLIGATION_TREE",
    "theorem_id": "THM-M-0996", "registry_id": "THM-M-0996-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator_sha, "root_node_id": f"{PREFIX}-ROOT",
    "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent; other graph semantics are non-proof.",
    "nodes": nodes, "graphs": graphs,
    "remaining_root_cut_set": [f"{PREFIX}-L-HALFSPACE", f"{PREFIX}-L-GENERAL"],
    "theorem_complete": False,
}

(ROOT / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(ROOT / "typed-graphs.json").write_text(json.dumps(typed, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator_sha}")
