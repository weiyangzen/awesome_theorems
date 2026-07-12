#!/usr/bin/env python3
"""Deterministically render the THM-M-1148 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ROWS = [
    ("ROOT", "root", "Exact Poisson integral formula on every positive-radius disk.", "Stage1Instances.THM_M_1148.PoissonIntegralFormula", "The exact frozen existential target.", "critical", "split-required"),
    ("S", "definition", "Freeze all statement, domain, normalization, and foundation choices.", "statement layer for PoissonIntegralFormula", "An unambiguous analytic target and trust policy.", "critical", "split-required"),
    ("S1", "definition", "Identify the open disk, closed disk, boundary circle, and positive radius.", "c : ℂ; R : ℝ; 0 < R; ball c R; closedBall c R; sphere c R", "The exact geometric domains used downstream.", "high", 7),
    ("S2", "normalization", "Fix mathlib's normalized circle average and Poisson kernel convention.", "circleAverage (poissonKernel c w • g) c R", "The formula with no extra 2*pi factor.", "critical", 8),
    ("S3", "branch", "Exclude the degenerate radius and distinguish interior from boundary points.", "0 < R; w ∈ ball c R; z ∈ sphere c R", "Legal radius and point regimes.", "high", 8),
    ("S4", "certificate", "Record the Lean foundation, axioms, and noncomputable integration boundary.", "axiom and declaration closure of the eventual root", "A release-time trust obligation.", "critical", 8),
    ("N", "reduction", "Normalize an arbitrary disk to the unit disk and transport the result back.", "affine disk/unit-disk equivalence package", "Reduction preserving data, kernel formula, and analytic properties.", "critical", "split-required"),
    ("N1", "transport", "The affine map z ↦ (z-c)/R identifies disk, closure, and circle with unit domains.", "planned Lean equivalences for ball c R, closedBall c R, sphere c R", "Domain membership transports in both directions.", "high", 18),
    ("N2", "transport", "Pull boundary data to the unit circle without losing ContinuousOn.", "ContinuousOn g (sphere c R) → ContinuousOn (fun ζ => g (c + R*ζ)) (sphere 0 1)", "Continuous normalized boundary data.", "high", 16),
    ("N3", "transport", "Push the unit-disk construction back and preserve harmonicity, continuity, trace, and formula.", "unit solution package → SolutionPackage c R g u", "A solution package on the original disk.", "critical", 30),
    ("B", "branch", "Prove continuity of the constructed function separately in the interior and at the boundary.", "ContinuousOn u (closedBall c R)", "Closed-disk continuity after exhaustive point splitting.", "critical", "split-required"),
    ("B1", "branch", "At an interior point, continuity follows from local regularity of the kernel integral.", "ContinuousWithinAt u (closedBall c R) w for w ∈ ball c R", "Interior branch of closed-disk continuity.", "high", 24),
    ("B2", "branch", "At a boundary point, the Poisson integral converges to the prescribed boundary value.", "Tendsto u (𝓝[ball c R] z) (𝓝 (g z)) for z ∈ sphere c R", "Boundary-limit branch.", "critical", 36),
    ("B3", "certificate", "The open disk and boundary circle exhaust the closed disk when R is positive.", "closedBall c R = ball c R ∪ sphere c R", "Exhaustiveness and branch recomposition.", "high", 12),
    ("C", "construction", "Construct the Poisson extension and package all root conclusions.", "∀ c R, 0 < R → ∀ g, ContinuousOn g (sphere c R) → ∃ u, SolutionPackage c R g u", "ConstructedSolution.", "critical", "split-required"),
    ("C1", "construction", "Define the interior Poisson integral from the normalized boundary data.", "u₀ w = circleAverage (poissonKernel c w • g) c R", "A candidate on the open disk.", "critical", 12),
    ("C2", "lemma", "Show the circle average defining the candidate is well-defined at every interior point.", "∀ w ∈ ball c R, IntegrableOnCircle (poissonKernel c w • g) c R", "Existence and finite value of each interior integral.", "high", 28),
    ("C3", "construction", "Extend the interior candidate to the boundary using g.", "u w = if w ∈ ball c R then u₀ w else g w", "A total function with an explicit boundary value.", "high", 12),
    ("L", "core_lemma", "Establish the analytic properties of the Poisson kernel needed by the construction.", "Poisson kernel analytic lemma package", "Harmonicity, normalization, concentration, and convergence inputs.", "critical", "split-required"),
    ("L1", "core_lemma", "The interior Poisson integral is harmonic as a function of its evaluation point.", "HarmonicOnNhd u₀ (ball c R)", "Root harmonicity conclusion for the candidate.", "critical", 55),
    ("L2", "core_lemma", "The Poisson kernel has normalized circle average one for an interior point.", "circleAverage (poissonKernel c w) c R = 1 for w ∈ ball c R", "Kernel mass normalization.", "critical", 32),
    ("L3", "core_lemma", "The kernel mass outside any boundary neighborhood tends to zero radially.", "planned uniform concentration estimate for poissonKernel", "Approximate-identity concentration.", "critical", 58),
    ("L4", "core_lemma", "Continuous boundary data on the circle is uniformly continuous.", "UniformContinuousOn g (sphere c R)", "A uniform boundary modulus used in the epsilon estimate.", "high", 24),
    ("L5", "core_lemma", "Split the boundary integral into near and far arcs and combine mass and concentration estimates.", "Poisson integral tends to g z as w → z within ball c R", "Boundary convergence for every z on the circle.", "critical", 72),
    ("X", "bridge", "Audit and use the pinned mathlib kernel, harmonicity, topology, and circle-integration APIs.", "Mathlib.Analysis.Complex.Harmonic.Poisson and transitive declarations", "Imported interface, provenance, and trust boundary.", "critical", 24),
    ("T", "terminal", "Compose construction, harmonicity, closed-disk continuity, trace, and the interior formula into the exact root.", "ConstructedSolution → PoissonIntegralFormula", "Exact child-to-root composition.", "critical", 9),
]

def fp(target):
    return hashlib.sha256(target.encode()).hexdigest()

def oid(short):
    return f"M1148-{short}"

obligations = []
nodes = []
for short, kind, human, target, output, risk, budget in ROWS:
    obligation = oid(short)
    fingerprint = "elaborated:4631cdf8cf607ec85b6c0e053d81966f967247daf9952a6edcbdfee6ac4016d8" if short == "ROOT" else f"planned:{fp(target)}"
    obligations.append({
        "obligation_id": obligation, "statement_fingerprint": fingerprint,
        "kind": kind, "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": None,
    })
    nodes.append({
        "node_id": f"THM-M-1148-{short}", "obligation_id": obligation, "kind": kind,
        "human_statement": human, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M4", "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-pinpoint-open",
        "provenance_id": "none" if short not in {"ROOT", "S", "S1", "S2", "S3", "T"} else "local:Statement.lean-or-ObligationTree.lean",
        "foundation_profile": "lean4-4.29.0-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "mathlib-8a178386ffc0f5fef0b77738bb5449d50efeea95/transitive-closure-pending",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": f"Premises: the declared child obligations and frozen domain hypotheses. Inference: {human} Output: {output} This budget is architectural, not proof evidence.",
        "public_readable_target": f"Stage1_Instances/THM-M-1148/obligation-tree.md#m1148-{short.lower()}",
        "validation_spec_id": f"VAL-M1148-{short}-PENDING",
        "status_boundary": "Architecture and interface only; no analytic proof body or closure is claimed.",
        "task_ids": ["S56-M-1148-OBLIGATION_TREE", "S56-M-1148-PROOF"],
        "owned_sources": [], "owner": "THM-M-1148 proof implementer",
        "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,source,toolchain,dependency change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1148-OBLIGATION_TREE",
    "theorem_id": "THM-M-1148", "registry_version": 1,
    "freeze_basis": "Exact elaborated statement plus a classical Poisson-integral proof architecture; eligibility is assigned independently of discovered closure, and the prior anchor audit supplies no proof credit.",
    "root_obligation_id": oid("ROOT"),
    "frozen_denominators": {"inventory": ids, "required_machine": ids, "required_human_source": ids, "required_readable": ids},
    "denominator_sha256": denominator, "append_only_delta": [], "obligations": obligations,
}

EDGE_SPECS = {
    "proof": [("ROOT", "T", "proof_requires"), ("T", "C", "proof_requires"), ("T", "L1", "proof_requires"), ("T", "B", "proof_requires"), ("T", "N3", "proof_requires"), ("C", "C1", "proof_requires"), ("C", "C2", "proof_requires"), ("C", "C3", "proof_requires"), ("C2", "X", "proof_requires"), ("L1", "X", "proof_requires"), ("B1", "L1", "proof_requires"), ("B2", "L5", "proof_requires"), ("B3", "S1", "proof_requires"), ("L5", "L2", "proof_requires"), ("L5", "L3", "proof_requires"), ("L5", "L4", "proof_requires"), ("N3", "N", "proof_requires"), ("N", "N1", "proof_requires"), ("N", "N2", "proof_requires")],
    "refinement": [("ROOT", x, "logical_decomposition") for x in ["S", "N", "B", "C", "L", "X", "T"]] + [("S", x, "logical_decomposition") for x in ["S1", "S2", "S3", "S4"]] + [("B", x, "logical_decomposition") for x in ["B1", "B2", "B3"]] + [("L", x, "logical_decomposition") for x in ["L1", "L2", "L3", "L4", "L5"]],
    "provenance": [("X", "S2", "provenance_of")],
    "evidence": [],
    "trust": [("ROOT", "S4", "trusts"), ("ROOT", "X", "trusts")],
    "documentation": [("ROOT", x, "documents") for x in ["S", "N", "B", "C", "L", "X", "T"]],
    "workflow": [("T", "C", "workflow_depends_on"), ("T", "B", "workflow_depends_on"), ("T", "L", "workflow_depends_on")],
}

graphs = {}
counter = 0
for name, specs in EDGE_SPECS.items():
    edges, incoming, outgoing = [], {}, {}
    for source, target, role in specs:
        counter += 1
        edge = {"edge_id": f"M1148-E{counter:03d}", "from": oid(source), "to": oid(target), "type": role}
        edges.append(edge)
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1148-OBLIGATION_TREE",
    "theorem_id": "THM-M-1148", "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "certificate_id": "M1148-COMP-ROOT-01", "parent": oid("ROOT"),
        "children": [oid("C"), oid("L1"), oid("B"), oid("N3")],
        "declaration": "Stage1Instances.THM_M_1148.ObligationTree.constructedSolution_to_root",
        "status": "interface_elaborated_children_open",
        "boundary": "The theorem consumes a ConstructedSolution hypothesis; it does not supply any open analytic child.",
    }],
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M4", "theorem_complete": False, "remaining_root_cut_set": [oid("C"), oid("L1"), oid("B"), oid("N3")]},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
print(f"rendered {len(obligations)} obligations, {counter} typed edges; denominator {denominator}")
