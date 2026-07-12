#!/usr/bin/env python3
"""Build the frozen THM-M-1333 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1333-OBLIGATION_TREE"
THEOREM = "THM-M-1333"
PREFIX = "M1333"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def planned(text: str) -> str:
    return "planned:v1:sha256:" + sha(text.encode())


specs = [
    ("ROOT", "root", "The exact finite-dimensional local Peano existence target.",
     "Stage1Instances.THM_M_1333.PeanoExistenceTarget", "The canonical proposition.", 8, "critical"),
    ("S-STATEMENT", "definition", "Preserve the open domain, joint continuity, positive symmetric interval, graph membership, and derivative-within encoding.",
     "Stage1Instances.THM_M_1333.{PeanoExistenceTarget,IsSolutionWithin}", "The exact input and output interfaces used by composition.", 10, "critical"),
    ("S-BOUNDARIES", "normalization", "Handle n = 0, positive radius, endpoint derivatives, and exclude uniqueness and global continuation.",
     "Boundary package for PeanoExistenceTarget", "No degenerate or neighboring theorem is silently substituted.", 12, "high"),
    ("S-FOUNDATION", "certificate", "Audit finite-dimensional compactness, integration, classical subsequence extraction, and the transitive trust boundary.",
     "Foundation and TCB certificate for every terminal body", "An accepted foundation profile covering all proof dependencies.", 12, "critical"),
    ("N-RECTANGLE", "normalization", "From openness and membership, choose a compact time-state box inside U and a positive uniform bound for f on it.",
     "Planned Lean signature: exists_compact_rectangle_and_bound", "Positive radii a,b and M with the rectangle in U and norm (f t x) <= M.", 24, "critical"),
    ("C-EULER", "construction", "Construct delayed Euler polygonal approximants on a common positive interval.",
     "Planned Lean signature: exists_delayedEulerApproximation", "A sequence of continuous polygonal curves with explicit mesh and integral-delay equation.", 38, "critical"),
    ("C-INVARIANTS", "construction", "Prove every approximant remains in the rectangle and is uniformly bounded and equicontinuous.",
     "Planned Lean signature: delayedEuler_invariants", "Common-domain containment and a uniform Lipschitz modulus for the approximants.", 34, "critical"),
    ("L-COMPACT", "bridge", "Apply finite-dimensional Arzela-Ascoli to extract a uniformly convergent subsequence.",
     "Planned Lean signature: exists_uniformlyConvergent_subsequence", "A continuous limit curve and uniform convergence on the selected interval.", 32, "critical"),
    ("L-INTEGRAL", "core_lemma", "Use uniform continuity of f on the compact box to pass the delayed integral equations to the limit.",
     "Planned Lean signature: limit_satisfies_integralEquation", "The limit satisfies x t = x0 + integral over t0..t of f s (x s).", 42, "critical"),
    ("L-DERIV", "bridge", "Apply the interval fundamental theorem of calculus to recover HasDerivWithinAt, including endpoints.",
     "Planned Lean signature: integralEquation_hasDerivWithinAt", "The limit curve has derivative f t (x t) within the closed interval.", 28, "critical"),
    ("L-ZERO-DIM", "lemma", "Close the n = 0 branch with the unique constant state curve while retaining a positive interval inside U.",
     "Planned Lean signature: peanoExistence_fin_zero", "PeanoExistenceTarget specialized to n = 0.", 20, "high"),
    ("B-DIM", "branch", "Split n = 0 from n > 0 and recompose the exhaustive dimension cases.",
     "Planned Lean signature: peanoExistence_of_zero_and_positive_dimension", "Existence for every natural dimension.", 14, "high"),
    ("T-SOLUTION", "transport", "Package the positive-dimensional limit curve, initial value, graph containment, and derivative result as IsSolutionWithin.",
     "Stage1Instances.THM_M_1333.isSolutionWithin_of_components", "The exact IsSolutionWithin conjunct required by the target.", 16, "high"),
    ("T-ASSEMBLE", "transport", "Quantify the selected radius and curve and discharge the exact canonical target from both dimension branches.",
     "Planned Lean signature: peanoExistenceTarget_of_dimension_branches", "Stage1Instances.THM_M_1333.PeanoExistenceTarget.", 18, "critical"),
    ("X-SOURCE", "certificate", "Pinpoint primary and modern sources for every compactness, approximation, limit, and differentiation node.",
     "Reviewed node-specific source crosswalk", "Human-source evidence without machine-proof credit.", 18, "critical"),
    ("X-PROVENANCE", "certificate", "Resolve every terminal declaration, body, revision, license, placeholder scan, dependency, and axiom report.",
     "Transitive terminal-body provenance and trust closure", "No anchor-only candidate or wrapper is credited as a proof body.", 20, "critical"),
]

ids = [f"{PREFIX}-{suffix}" for suffix, *_ in specs]
statement_hash = sha((HERE / "Statement.lean").read_bytes())
anchor_hash = sha((HERE / "anchor-audit.json").read_bytes())

obligations = []
nodes = []
for suffix, kind, human, formal, output, budget, risk in specs:
    oid = f"{PREFIX}-{suffix}"
    fp = ("lean-source-sha256:" + statement_hash) if suffix in {"ROOT", "S-STATEMENT"} else planned(formal + "\n" + human + "\n" + output)
    machine = "not_applicable" if suffix == "X-SOURCE" else ("informational" if suffix == "X-PROVENANCE" else "required")
    human_eligibility = "required" if suffix not in {"S-STATEMENT", "S-FOUNDATION", "X-PROVENANCE"} else "not_applicable"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human_eligibility, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if suffix == "X-SOURCE" else ("release_overlay_no_proof_credit" if suffix == "X-PROVENANCE" else None),
        "terminal_proof_body_id": None,
    })
    if kind in {"root", "branch", "transport"}:
        ledger = [
            "Bind the exact statement fingerprints of every declared proof child.",
            "Consume every declared child output without adding an undeclared premise.",
            f"Derive the declared output: {output}",
            "Record a kernel-checked child-to-parent composition declaration before closure.",
        ]
    else:
        ledger = [
            "Freeze the exact local context and named premises.",
            f"Establish the transition: {human}",
            f"Derive the declared output: {output}",
            "Pass only that output through the declared proof edge; retain all boundary conditions.",
        ]
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M3" if suffix in {"S-STATEMENT", "T-SOLUTION"} else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-bounded; primary-node-map-pending" if human_eligibility == "required" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/finite-dimensional-analysis-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical approximation or external oracle receives proof credit",
        "step_budget": budget, "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-1333/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING" if suffix not in {"S-STATEMENT", "T-SOLUTION"} else f"VAL-{oid}-LEAN",
        "status_boundary": "Frozen interface only; the listed mathematical result and root closure remain open.",
        "task_ids": [ITEM, "S56-M-1333-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1333/ObligationTree.lean"] if suffix in {"S-STATEMENT", "T-SOLUTION"} else [],
        "owner": "THM-M-1333 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if suffix in {"S-STATEMENT", "T-SOLUTION"} else None,
                     "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if suffix in {"S-STATEMENT", "T-SOLUTION"} else "open"},
    })

denominators = {
    "inventory": ids,
    "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
    "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
    "required_readable": ids,
    "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
}
denominator_hash = sha(json.dumps(denominators, sort_keys=True, separators=(",", ":")).encode())

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated continuity-only statement and bounded anchor audit; delayed-Euler/Arzela-Ascoli route selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator_hash,
    "frozen_denominators": denominators,
    "delta_policy": "Any semantic correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("T-ASSEMBLE", "ROOT"), ("S-STATEMENT", "T-ASSEMBLE"), ("S-BOUNDARIES", "T-ASSEMBLE"),
    ("S-FOUNDATION", "T-ASSEMBLE"), ("B-DIM", "T-ASSEMBLE"), ("L-ZERO-DIM", "B-DIM"),
    ("T-SOLUTION", "B-DIM"), ("N-RECTANGLE", "T-SOLUTION"), ("L-DERIV", "T-SOLUTION"),
    ("L-INTEGRAL", "L-DERIV"), ("L-COMPACT", "L-INTEGRAL"), ("C-INVARIANTS", "L-COMPACT"),
    ("C-EULER", "C-INVARIANTS"),
]
refinement_pairs = [("S-STATEMENT", "ROOT"), ("S-BOUNDARIES", "ROOT"), ("N-RECTANGLE", "ROOT")]
provenance_pairs = [("X-PROVENANCE", s) for s, *_ in specs if s != "X-PROVENANCE"]
evidence_pairs = [("S-STATEMENT", "ROOT"), ("X-SOURCE", "ROOT"), ("X-PROVENANCE", "ROOT")]
trust_pairs = [("S-FOUNDATION", "ROOT"), ("X-PROVENANCE", "S-FOUNDATION")]
documentation_pairs = [(s, "ROOT") for s, *_ in specs if s != "ROOT"]
workflow_pairs = [("X-SOURCE", "X-PROVENANCE"), ("X-PROVENANCE", "S-FOUNDATION"), ("S-STATEMENT", "C-EULER"), ("C-EULER", "T-ASSEMBLE")]


def graph(name, relation, pairs):
    edges, incoming, outgoing = [], {}, {}
    for i, (a, b) in enumerate(pairs, 1):
        eid = f"{name.upper()}-{i:02d}"
        a, b = f"{PREFIX}-{a}", f"{PREFIX}-{b}"
        edges.append({"edge_id": eid, "type": relation, "from": a, "to": b})
        outgoing.setdefault(a, []).append(eid)
        incoming.setdefault(b, []).append(eid)
    return {"relation": relation, "edges": edges, "out": outgoing, "in": incoming}


graphs = {
    "proof": graph("proof", "proof_requires", proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", refinement_pairs),
    "provenance": graph("provenance", "provenance_of", provenance_pairs),
    "evidence": graph("evidence", "evidence_for", evidence_pairs),
    "trust": graph("trust", "trusts", trust_pairs),
    "documentation": graph("documentation", "documents", documentation_pairs),
    "workflow": graph("workflow", "workflow_depends_on", workflow_pairs),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1333-OBLIGATIONS-v1", "registry_denominator_sha256": denominator_hash,
    "root_node_id": f"{PREFIX}-ROOT",
    "edge_direction": "Proof and refinement edges run required child to parent; other graph meanings are named by relation.",
    "nodes": nodes, "graphs": graphs,
    "validation_recipes": [
        {"recipe_id": "VAL-M1333-OBLIGATION-STRUCTURE", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1333/check_obligation_tree.py"],
         "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "record exact output"}], "covered_obligation_ids": ids,
         "covered_declarations": []},
        {"recipe_id": "VAL-M1333-OBLIGATION-LEAN", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1333/check_obligation_lean.py"],
         "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "record axiom report"}],
         "covered_obligation_ids": [f"{PREFIX}-S-STATEMENT", f"{PREFIX}-T-SOLUTION"],
         "covered_declarations": ["Stage1Instances.THM_M_1333.isSolutionWithin_of_components"]},
    ],
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": [f"{PREFIX}-C-EULER", f"{PREFIX}-L-COMPACT", f"{PREFIX}-L-INTEGRAL", f"{PREFIX}-L-DERIV"],
                         "root_machine_debt": "M4"},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

lines = ["# THM-M-1333 obligation tree", "", "The frozen route is delayed Euler approximation followed by finite-dimensional Arzela-Ascoli, passage to the integral equation, and the fundamental theorem of calculus. Every mathematical node below is open unless explicitly described as an interface check; no proof of Peano existence is claimed.", "", "## Proof flow", ""]
for suffix, kind, human, formal, output, budget, risk in specs:
    oid = f"{PREFIX}-{suffix}"
    lines += [f"### {oid}", "", f"Kind: `{kind}`. Risk: `{risk}`. Step budget: `{budget}`.", "", human, "", f"Formal target: `{formal}`", "", f"Output: {output}", "", "Semantic ledger:"]
    node = next(n for n in nodes if n["obligation_id"] == oid)
    lines += [f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)]
    lines += ["", node["status_boundary"], ""]
lines += ["## Typed overlays", "", "The JSON bundle separates proof, refinement, provenance, evidence, trust, documentation, and workflow edges. Source and provenance overlays cannot close machine obligations or add proof-body credit.", "", "## Closure boundary", "", "All fourteen machine-required obligations are open. The first critical root cut is `M1333-C-EULER`, `M1333-L-COMPACT`, `M1333-L-INTEGRAL`, and `M1333-L-DERIV`. Primary-source node review, terminal provenance, readable reconstruction, composition bodies, and release validation also remain open.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))

print(f"wrote {len(ids)} obligations; denominator {denominator_hash}")
