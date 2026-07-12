#!/usr/bin/env python3
"""Generate the frozen THM-M-0168 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT_HASH = "b5cef8a8bb3b5505be6670f226315884282c53bb0040c30345f4fb0dc33254f5"

specs = [
    ("ROOT", "root", "Exact two-dimensional Bernstein minimal-graph target.", "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget", "Exact canonical theorem", "critical", "M2", ["consume DERIVATIVE-RIGIDITY", "consume INTEGRATE", "apply compose_root"]),
    ("S-INTERFACE", "definition", "Freeze the entire R^2 domain, C2 regularity, Frechet coordinate derivatives, minimal-surface PDE, and affine conclusion.", "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget", "Exact analytic interface", "high", "M3", ["fix domain and regularity", "fix coordinate derivatives", "fix PDE signs and indices", "fix affine conclusion"]),
    ("C-GRAPH", "construction", "Construct the graph immersion p -> (p.1,p.2,u p), its induced metric, unit normal, and second fundamental form.", "planned signature: GraphGeometry u", "Graph geometric data and invariants", "high", "M4", ["define graph map", "prove immersion", "compute induced metric", "construct oriented unit normal", "define second fundamental form"]),
    ("N-PDE-MINIMAL", "transport", "Transport the frozen coordinate PDE to zero mean curvature of the constructed graph in the required direction.", "planned signature: PDE u -> MeanCurvature (graph u) = 0", "Minimality of the graph", "critical", "M4", ["differentiate graph map", "compute normal", "compute mean curvature numerator", "use positive metric denominator", "rewrite the PDE"]),
    ("L-STABILITY", "core_lemma", "Prove the entire minimal graph is stable using its positive vertical normal component.", "planned signature: MinimalGraph u -> Stable (graph u)", "Stability inequality for compactly supported tests", "critical", "M4", ["identify positive Jacobi field", "derive Jacobi equation", "perform compact-support integration by parts", "derive stability inequality"]),
    ("C-CUTOFF", "construction", "Construct logarithmic cutoffs on the graph with controlled Dirichlet energy and justify exhaustion of the noncompact surface.", "planned signature: LogCutoffExhaustion (graph u)", "Cutoff family and vanishing-energy bound", "high", "M4", ["define intrinsic/extrinsic annuli", "construct cutoff", "prove compact support", "bound gradient energy", "prove exhaustion limit"]),
    ("L-CURVATURE", "core_lemma", "Combine stability, the minimal-surface curvature identity, and logarithmic cutoffs to force the second fundamental form to vanish everywhere.", "planned signature: Stable graph -> LogCutoffExhaustion graph -> SecondFundamentalForm graph = 0", "Vanishing second fundamental form", "critical", "M4", ["insert cutoff into stability", "use curvature identity", "control boundary terms", "pass to exhaustion limit", "deduce integral vanishing", "upgrade to pointwise vanishing"]),
    ("L-DERIVATIVE-RIGIDITY", "core_lemma", "Deduce that both coordinate first derivatives of u are constant from flatness of its connected entire graph.", "Stage1Instances.THM_M_0168_Obligations.DerivativeRigidity", "Constant coordinate derivatives", "critical", "M4", ["consume graph geometry", "consume PDE-minimal transport", "consume stability", "consume cutoff package", "consume curvature vanishing", "translate flat normal to constant gradient"]),
    ("T-INTEGRATE", "bridge", "Integrate constant Frechet coordinate derivatives along line segments in R^2 to obtain the global affine formula.", "Stage1Instances.THM_M_0168_Obligations.ConstantPartialsToAffine", "Affine representation of u", "high", "M4", ["choose c = u (0,0)", "restrict u to a line segment", "compute one-variable derivative", "apply constant-derivative theorem", "evaluate endpoints"]),
    ("X-SOURCE", "terminal", "Bind every analytic and geometric step to pinpoint human sources before H0 can be claimed.", "planned source crosswalk and independent review receipt", "Human provenance boundary", "high", "M5", ["pin primary source", "pin modern exposition", "map assumptions and notation", "map every proof obligation", "record errata and review"]),
    ("X-TRUST", "terminal", "Classify imports, declarations, axioms, automation, and computation for every eventual proof body.", "planned transitive declaration and axiom reports", "Trust boundary classification", "critical", "M3", ["bind toolchain and mathlib", "inspect dependencies", "inspect axioms", "reject unknown executable boundaries"]),
]

def node(short, kind, human, formal, output, risk, mdebt, ledger):
    oid = f"M0168-{short}"
    fp = f"lean-expr:{ROOT_HASH}" if short in {"ROOT", "S-INTERFACE"} else f"planned:{oid}-v1"
    anchor = short.lower().replace("-", "-")
    return {
        "obligation_id": oid, "node_id": f"THM-M-0168-{short}", "kind": kind,
        "statement_fingerprint": fp, "human_statement": human, "formal_target": formal,
        "output": output, "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "not_applicable" if short == "X-TRUST" else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": None, "human_debt": "H1", "machine_debt": mdebt,
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if short == "X-TRUST" else f"SRC-M0168-{short}",
        "provenance_id": "none", "foundation_profile": "LEAN4-MATHLIB-CLASSICAL-PENDING-1",
        "tcb_profile": "LEAN4-PINNED-PENDING-1", "computation_record": "none",
        "step_budget": len(ledger), "semantic_step_ledger": [f"{short}-{i+1}: {x}" for i, x in enumerate(ledger)],
        "public_readable_target": f"Stage1_Instances/THM-M-0168/obligation-tree.md#{anchor}",
        "validation_spec_id": "VAL-M0168-OBLIGATION-TREE",
        "status_boundary": "This obligation is architectural and open unless its machine debt says otherwise; it supplies no theorem-completion credit.",
        "task_ids": ["S56-M-0168-OBLIGATION_TREE", "S56-M-0168-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0168/ObligationTree.lean"] if short in {"ROOT", "L-DERIVATIVE-RIGIDITY", "T-INTEGRATE"} else [],
        "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer required",
        "validity": {"validated_at": "2026-07-12", "review_due": "pending master acceptance", "invalidation_inputs": ["canonical target", "registry", "typed graphs", "toolchain", "proof route"], "revocation_state": "active_provisional"},
    }

nodes = [node(*s) for s in specs]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "registry_version": 1,
    "item_id": "S56-M-0168-OBLIGATION_TREE", "theorem_id": "THM-M-0168",
    "frozen_before_proof_execution": True, "canonical_root_expression_sha256": ROOT_HASH,
    "status_observation_boundary": "The bounded anchor audit was read only to set provenance debt; eligibility, nodes, and denominators do not depend on discovered closure.",
    "obligations": nodes,
}

def edge(a, typ, b, **extra):
    return {"from": f"M0168-{a}", "type": typ, "to": f"M0168-{b}", **extra}

proof_requires = [("ROOT", "L-DERIVATIVE-RIGIDITY"), ("ROOT", "T-INTEGRATE"),
    ("L-DERIVATIVE-RIGIDITY", "C-GRAPH"), ("L-DERIVATIVE-RIGIDITY", "N-PDE-MINIMAL"),
    ("L-DERIVATIVE-RIGIDITY", "L-STABILITY"), ("L-DERIVATIVE-RIGIDITY", "C-CUTOFF"),
    ("L-DERIVATIVE-RIGIDITY", "L-CURVATURE"), ("L-STABILITY", "C-GRAPH"),
    ("L-STABILITY", "N-PDE-MINIMAL"), ("L-CURVATURE", "L-STABILITY"),
    ("L-CURVATURE", "C-CUTOFF")]
ids = [n["obligation_id"] for n in nodes]
graphs = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0168-OBLIGATION_TREE",
    "theorem_id": "THM-M-0168", "registry_version": 1,
    "graphs": {
        "proof": [edge(a, "proof_requires", b) for a, b in proof_requires] +
          [edge("ROOT", "composes", b, certificate="Stage1Instances.THM_M_0168_Obligations.compose_root") for b in ("L-DERIVATIVE-RIGIDITY", "T-INTEGRATE")],
        "refinement": [edge("ROOT", "logical_decomposition", x) for x in ("S-INTERFACE", "L-DERIVATIVE-RIGIDITY", "T-INTEGRATE")],
        "provenance": [{"from": "M0168-S-INTERFACE", "type": "provenance_of", "to": f"statement-validation:{ROOT_HASH[:8]}"}, {"from": "M0168-X-SOURCE", "type": "source_map", "to": "source-statement-crosswalk.md"}],
        "evidence": [{"from": f"statement-validation:{ROOT_HASH[:8]}", "type": "evidence_for", "to": "M0168-S-INTERFACE"}],
        "trust": [edge(x.removeprefix("M0168-"), "trusts", "X-TRUST") for x in ids if x != "M0168-X-TRUST"],
        "documentation": [{"from": x, "type": "documents", "to": next(n["public_readable_target"] for n in nodes if n["obligation_id"] == x)} for x in ids],
        "workflow": [
          {"from": "S56-M-0168-OBLIGATION_TREE", "type": "workflow_depends_on", "to": "S56-M-0168-ANCHOR_AUDIT"},
          {"from": "S56-M-0168-PROOF", "type": "workflow_depends_on", "to": "S56-M-0168-OBLIGATION_TREE"},
          {"from": "S56-M-0168-VALIDATION", "type": "workflow_depends_on", "to": "S56-M-0168-PROOF"},
          {"from": "S56-M-0168-RELEASE", "type": "workflow_depends_on", "to": "S56-M-0168-VALIDATION"}],
    },
    "root_cut_set": ["M0168-C-GRAPH", "M0168-N-PDE-MINIMAL", "M0168-L-STABILITY", "M0168-C-CUTOFF", "M0168-L-CURVATURE", "M0168-L-DERIVATIVE-RIGIDITY", "M0168-T-INTEGRATE"],
    "coverage_denominators": {"canonical_obligations": ids,
      "required_logical_leaves": ["M0168-S-INTERFACE", "M0168-C-GRAPH", "M0168-N-PDE-MINIMAL", "M0168-C-CUTOFF", "M0168-T-INTEGRATE", "M0168-X-SOURCE", "M0168-X-TRUST"],
      "required_readable": ids},
    "closure_metrics_observed": False,
    "status_boundary": "Registry, route, typed graphs, and denominators are frozen. All theorem-bearing packages remain open; no proof or completion promotion is claimed.",
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", graphs)):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
    print(name, hashlib.sha256((HERE / name).read_bytes()).hexdigest())
