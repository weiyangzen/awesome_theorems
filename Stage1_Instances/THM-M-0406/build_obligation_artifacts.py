#!/usr/bin/env python3
"""Build the frozen THM-M-0406 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATEMENT_HASH = "9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec"
REGISTRY_ID = "THM-M-0406-OBLIGATIONS-v1"

# id, kind, risk, source-required, human statement, formal target, output, budget, ledger, source id
SPECS = [
    ("M0406-ROOT", "root", "critical", True, "Corvaja--Zannier Theorem 1 with the exact frozen binders and conclusion.", "Stage1Instances.THMM0406.CorvajaZannierTheoremOne", "The canonical proposition.", 8, ["Obtain the exact surface-degeneracy engine.", "Apply the checked engine-to-root adapter."], "SRC-CZ-2004-THM1"),
    ("M0406-S-DEFINITIONS", "definition", "high", True, "The abstract surface, boundary, point, curve, and S-integrality interfaces faithfully encode every source notion used by the theorem.", "Stage1Instances.THMM0406.{SurfaceData,IntegralPointData,HasTheoremOneBoundary}", "Well-scoped definitions matching the source crosswalk.", 70, ["Audit the projective surface and affine-open fields.", "Audit boundary components and intersection pairing.", "Audit rational and S-integral point predicates.", "Audit proper-curve containment."], "SRC-CZ-2004-THM1"),
    ("M0406-S-FOUNDATION", "terminal", "critical", False, "The eventual proof has an accepted transitive axiom, dependency, computation, and TCB closure.", "planned root axiom/dependency report", "Accepted foundation and trust closure.", 30, ["Resolve all terminal declarations.", "Extract transitive constants and axioms.", "Compare against the pinned foundation profile."], "not-applicable"),
    ("M0406-N-BOUNDARY", "normalization", "critical", True, "Normalize the weighted boundary divisors and their pairwise intersection condition into the form used by the auxiliary-function construction.", "planned Lean boundary-normalization theorem", "Normalized divisor and intersection data.", 85, ["Enumerate the finite boundary family.", "Preserve distinctness and the no-triple-point hypothesis.", "Normalize positive weights and the common intersection constant.", "Transport every pairwise equality."], "SRC-CZ-2004-SEC2"),
    ("M0406-N-INTEGRAL", "normalization", "critical", True, "Translate S-integrality on the affine open into local height and valuation bounds at all places outside S.", "planned Lean S-integrality-to-local-heights theorem", "Uniform outside-S local bounds for every selected point.", 95, ["Choose compatible local Weil functions.", "Use finiteness of S.", "Derive the outside-S bounds.", "Track constants uniformly over the point set."], "SRC-CZ-2004-SEC2"),
    ("M0406-C-AUXILIARY", "construction", "critical", True, "Construct rational functions and sections adapted to multiples of the boundary divisors.", "planned Lean auxiliary-sections construction", "Functions with controlled poles, zeros, and dimension estimates.", 100, ["Choose sufficiently divisible multiples.", "Build Riemann--Roch section spaces.", "Select bases with prescribed boundary orders.", "Prove pole and dimension estimates.", "Record choice independence needed downstream."], "SRC-CZ-2004-SEC2"),
    ("M0406-L-HEIGHT-INEQUALITY", "core_lemma", "critical", True, "Convert the auxiliary sections and S-integrality bounds into the global height inequality required by the Subspace Theorem.", "planned Lean global-height inequality", "A quantitative product-of-linear-forms inequality.", 100, ["Evaluate sections at an integral point.", "Sum local estimates over all places.", "Apply the product formula.", "Control exceptional zeros and constants.", "Derive the strict Subspace-Theorem exponent."], "SRC-CZ-2004-SEC2"),
    ("M0406-X-SUBSPACE", "bridge", "critical", True, "Apply the quantitative Schmidt Subspace Theorem to the constructed linear forms over the number field.", "planned exact Lean Subspace-Theorem bridge", "Finitely many exceptional proper linear subspaces.", 60, ["Instantiate the number-field theorem.", "Verify nondegeneracy of each local linear-form family.", "Supply the global height inequality.", "Obtain a finite exceptional family."], "SRC-EVERTSE-SUBSPACE"),
    ("M0406-B-EXCEPTIONAL", "branch", "critical", True, "For each exceptional linear relation, its pullback to the surface either is identically zero or cuts out a proper algebraic locus.", "planned Lean exceptional-relation dichotomy", "A finite family of proper closed loci containing all relevant points.", 90, ["Split on whether the pulled-back relation vanishes identically.", "Exclude the identically-zero case using basis independence.", "Construct the zero locus in the remaining case.", "Prove it is proper.", "Recombine the finite branches."], "SRC-CZ-2004-SEC2"),
    ("M0406-L-DIMENSION-DROP", "core_lemma", "critical", True, "A proper closed locus arising on the geometrically irreducible nonsingular surface has curve-dimensional support for the selected points.", "planned Lean surface dimension-drop theorem", "A finite union of curves containing the exceptional points.", 85, ["Use geometric irreducibility to rule out the whole surface.", "Pass to irreducible components.", "Bound component dimension by one.", "Discard components containing no selected points."], "SRC-CZ-2004-SEC2"),
    ("M0406-C-CURVE-UNION", "construction", "high", True, "Combine the finitely many exceptional curve components into one curve on the affine open and prove it is proper.", "planned Lean finite-curve-union construction", "One proper curve containing every S-integral rational point.", 75, ["Collect the finite exceptional components.", "Intersect/restrict them to the affine open.", "Form their finite union.", "Prove curvehood, properness, and point containment."], "SRC-CZ-2004-THM1"),
    ("M0406-T-ENGINE", "terminal", "critical", True, "Compose normalization, auxiliary functions, heights, Subspace Theorem, and geometric descent into the exact SurfaceDegeneracyEngine.", "Stage1Instances.THMM0406.SurfaceDegeneracyEngine", "The premise consumed by the checked root adapter.", 40, ["Normalize boundary and integral-point data.", "Construct auxiliary sections and the height inequality.", "Apply the Subspace-Theorem bridge.", "Descend exceptional subspaces to a proper curve."], "SRC-CZ-2004-THM1"),
    ("M0406-T-ROOT-ADAPTER", "transport", "high", False, "Translate the engine conclusion to the definitionally identical canonical root.", "Stage1Instances.THMM0406.corvajaZannierTheoremOne_of_engine", "Stage1Instances.THMM0406.CorvajaZannierTheoremOne.", 5, ["Consume the exact engine premise.", "Return it at the unfolded canonical target."], "not-applicable"),
    ("M0406-X-PROVENANCE", "terminal", "critical", False, "Every eventual proof body, imported theorem, computation, and source boundary has content-addressed provenance.", "planned machine-derived provenance closure", "Complete origin and dependency inventory.", 40, ["Resolve terminal proof bodies.", "Hash origins and dependencies.", "Bind validation receipts to this registry."], "not-applicable"),
]


def obligation(spec):
    oid, kind, risk, source, *_ = spec
    return {"obligation_id": oid, "statement_fingerprint": f"lean-sha256:{STATEMENT_HASH}" if oid == "M0406-ROOT" else f"planned-id:{oid}:v1", "kind": kind, "root_relevant": True, "machine_eligibility": "required", "human_source_eligibility": "required" if source else "not_applicable", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": None}


obligations = [obligation(s) for s in SPECS]
KEYS = ["obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason"]
projection = [{k: o[k] for k in KEYS} for o in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "registry_id": REGISTRY_ID,
    "theorem_id": "THM-M-0406", "item_id": "S56-M-0406-OBLIGATION_TREE",
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": {"canonical_declaration": "Stage1Instances.THMM0406.CorvajaZannierTheoremOne", "statement_source_sha256": STATEMENT_HASH, "source_inventory": "anchor-audit.json", "architecture_rule": "The source proof route through auxiliary sections, heights, the Subspace Theorem, exceptional loci, and curve descent is frozen independently of Lean candidate availability."},
    "denominator_projection": "Registry-order objects restricted to the nine eligibility keys and serialized with sorted keys and compact separators.",
    "denominator_sha256": denominator, "obligations": obligations,
    "eligibility_counts": {"total": len(obligations), "root_relevant": len(obligations), "machine_required": len(obligations), "human_source_required": sum(o["human_source_eligibility"] == "required" for o in obligations), "readable_required": len(obligations), "informational": 0},
    "status_observed_after_freeze": {"closed_obligations": [], "root_machine_debt": "M4"},
    "append_only_delta": [], "status_boundary": "The registry freezes scope and denominators only; it supplies no Subspace Theorem or surface-degeneracy proof credit."
}


def node(spec):
    oid, kind, _, _, human, formal, output, budget, ledger, source = spec
    checked = oid == "M0406-T-ROOT-ADAPTER"
    return {"node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": human, "formal_target": formal, "output": output, "human_debt": "H1", "machine_debt": "M4", "readability_debt": "R3" if budget < 70 else "R4", "evidence_ids": [], "source_crosswalk_id": source, "provenance_id": "PROV-LOCAL-CHECKED-ADAPTER" if checked else "none", "foundation_profile": "LEAN4-MATHLIB-CLASSICAL-v1", "tcb_profile": "LEAN4-PINNED-v1", "computation_record": "none", "step_budget": budget, "semantic_step_ledger": ledger, "public_readable_target": f"Stage1_Instances/THM-M-0406/obligation-tree.md#{oid.lower()}", "validation_spec_id": "VAL-M0406-OBLIGATION-TREE", "status_boundary": "The adapter elaborates, but its central engine premise remains open." if checked else "Open architecture node; no proof-body closure is credited.", "task_ids": ["S56-M-0406-OBLIGATION_TREE", "S56-M-0406-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0406/ObligationTree.lean" if checked or oid in {"M0406-ROOT", "M0406-T-ENGINE"} else "Stage1_Instances/THM-M-0406/typed-graphs.json"], "owner": "S56-M-0406 execution lane", "reviewer": "independent integration lane", "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "on invalidation", "invalidation_inputs": ["statement hash", "registry hash", "proof implementation"], "revocation_state": "provisional" if checked else "open"}}


def graph(name, edge_type, pairs):
    prefixes = {"proof": "P", "refinement": "R", "provenance": "PV", "evidence": "E", "trust": "TR", "documentation": "D", "workflow": "W"}
    edges, out, incoming = [], {}, {}
    for i, (src, dst) in enumerate(pairs, 1):
        eid = f"{prefixes[name]}{i:02d}"
        edges.append({"edge_id": eid, "type": edge_type, "from": src, "to": dst})
        out.setdefault(src, []).append(eid); incoming.setdefault(dst, []).append(eid)
    return {"edges": edges, "out": out, "in": incoming}


proof_pairs = [("M0406-ROOT", "M0406-T-ROOT-ADAPTER"), ("M0406-T-ROOT-ADAPTER", "M0406-T-ENGINE"), ("M0406-T-ENGINE", "M0406-N-BOUNDARY"), ("M0406-T-ENGINE", "M0406-N-INTEGRAL"), ("M0406-T-ENGINE", "M0406-C-AUXILIARY"), ("M0406-T-ENGINE", "M0406-L-HEIGHT-INEQUALITY"), ("M0406-T-ENGINE", "M0406-X-SUBSPACE"), ("M0406-T-ENGINE", "M0406-B-EXCEPTIONAL"), ("M0406-T-ENGINE", "M0406-L-DIMENSION-DROP"), ("M0406-T-ENGINE", "M0406-C-CURVE-UNION")]
graphs = {
    "proof": graph("proof", "proof_requires", proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", [("M0406-ROOT", "M0406-S-DEFINITIONS")]),
    "provenance": graph("provenance", "provenance_of", [("M0406-X-PROVENANCE", "M0406-ROOT")]),
    "evidence": graph("evidence", "evidence_for", []),
    "trust": graph("trust", "trusts", [("M0406-ROOT", "M0406-S-FOUNDATION"), ("M0406-ROOT", "M0406-X-PROVENANCE")]),
    "documentation": graph("documentation", "documents", [("M0406-ROOT", "M0406-S-DEFINITIONS"), ("M0406-ROOT", "M0406-T-ENGINE")]),
    "workflow": graph("workflow", "workflow_depends_on", proof_pairs),
}
typed = {"schema_version": "stage1-typed-graphs/1.0", "theorem_id": "THM-M-0406", "registry_id": REGISTRY_ID, "edge_direction": "Edges run from consumer/parent to required child/support; reciprocal adjacency is explicit.", "nodes": [node(s) for s in SPECS], "graphs": graphs, "closure_boundary": {"root_machine_debt": "M4", "closed_obligations": [], "minimal_open_root_cut_set": ["M0406-T-ENGINE"], "checked_interfaces_not_closed": ["M0406-T-ROOT-ADAPTER"], "composition_certificates": ["Stage1Instances.THMM0406.corvajaZannierTheoremOne_of_engine"], "audit_complete": False, "theorem_complete": False}}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", typed)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges; denominator {denominator}")
