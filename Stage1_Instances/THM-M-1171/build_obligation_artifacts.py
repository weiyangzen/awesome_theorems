#!/usr/bin/env python3
"""Build the frozen THM-M-1171 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1171-OBLIGATION_TREE"
ROOT = "M1171-ROOT"

SPECS = [
    (ROOT, "root", "The frozen whole-space Calderon-Zygmund Hessian estimate.", "Stage1Instances.THM_M_1171.CalderonZygmundEstimateTarget", "The exact canonical target.", "critical", "H2", "M4"),
    ("M1171-S-DEFINITIONS", "definition", "Fix Euclidean space, Hessian, Laplacian, exponent, measure, and binder order.", "Statement.lean definitions and ExpandedTarget", "The exact analytic objects used by the root.", "high", "not_applicable", "M3"),
    ("M1171-S-BOUNDARIES", "normalization", "Retain n >= 1 and 1 < p < infinity; exclude all endpoint and bounded-domain variants.", "Boundary package for the canonical target", "No broadened or substituted theorem enters composition.", "high", "H2", "M4"),
    ("M1171-S-FOUNDATION", "certificate", "Freeze classical analysis, choice, computation, and TCB policies.", "Foundation and trust certificate", "An accepted foundation profile for all terminal bodies.", "critical", "not_applicable", "M4"),
    ("M1171-N-SCHWARTZ", "normalization", "Transport a smooth compactly supported real function to the Schwartz/Fourier domain.", "ContDiff plus HasCompactSupport implies the required Schwartz regularity", "A Fourier-transformable test function with derivative identities.", "critical", "H2", "M4"),
    ("M1171-N-COMPLEX", "transport", "Complexify the scalar function and preserve the relevant Lp norms and derivatives.", "Real-to-complex Fourier transport", "A complex Fourier formulation equivalent to the real component estimates.", "high", "H2", "M4"),
    ("M1171-L-FOURIER-DERIV", "core_lemma", "Identify Fourier transforms of every second partial derivative and of the Laplacian.", "F(partial_i partial_j u) and F(laplacian u) identities", "The multiplier relation away from frequency zero.", "critical", "H2", "M4"),
    ("M1171-C-MULTIPLIER", "construction", "Define m_ij(xi) = xi_i xi_j / |xi|^2 off zero and choose its value at zero.", "Measurable homogeneous multiplier family m_ij", "A total measurable multiplier with the correct punctured-space symbol.", "critical", "H2", "M4"),
    ("M1171-L-MIHLIN", "bridge", "Prove uniform derivative bounds for m_ij and apply strong Lp multiplier boundedness for 1 < p < infinity.", "LpBounded (fourierMultiplier m_ij) p", "A constant depending only on n and p for every component multiplier.", "critical", "H2", "M4"),
    ("M1171-L-ZERO-FREQ", "lemma", "Show the arbitrary value of m_ij at frequency zero does not alter the Lp identity.", "Almost-everywhere zero-frequency removal", "A valid global multiplier identity from the punctured identity.", "high", "H2", "M4"),
    ("M1171-T-COMPONENT", "composition", "Compose Fourier identities, the multiplier bound, and zero-frequency removal.", "eLpNorm (partial_i partial_j u) p <= C * eLpNorm (laplacian u) p", "All n^2 second partial derivatives obey one uniform estimate.", "critical", "H2", "M4"),
    ("M1171-L-FDERIV-PARTIAL", "transport", "Identify Hessian evaluations on standard basis vectors with second partial derivatives.", "hessian u x e_i e_j = partial_i partial_j u x", "Component estimates for the dossier's Frechet Hessian.", "critical", "H2", "M4"),
    ("M1171-L-TRACE", "transport", "Identify the dossier's trace definition of laplacian with the Fourier-side Laplacian.", "laplacian u = sum_i partial_i partial_i u", "The exact right-hand side used by the root.", "critical", "H2", "M4"),
    ("M1171-L-OPNORM", "core_lemma", "Bound the finite-dimensional bilinear operator norm by the sum of standard-basis components.", "norm A <= K(n) * sum_i sum_j norm (A e_i e_j)", "A dimension-only pointwise Hessian norm bound.", "critical", "H2", "M4"),
    ("M1171-L-LP-ASSEMBLY", "core_lemma", "Lift the finite component sum and scalar constants through eLpNorm.", "eLpNorm of Hessian norm controlled by component eLpNorms", "A single Hessian eLpNorm estimate with a finite-dimensional constant.", "critical", "H2", "M4"),
    ("M1171-T-ASSEMBLE", "composition", "Combine component bounds, derivative transports, and finite-dimensional norm assembly.", "Canonical inequality for fixed n p u", "The root inequality with a nonnegative constant independent of u.", "critical", "H2", "M4"),
    ("M1171-X-SOURCE", "source_boundary", "Pinpoint primary and modern sources for each analytic bridge and check assumptions and errata.", "Reviewed node-specific source crosswalk", "H-state evidence without machine-proof credit.", "high", "H2", "not_applicable"),
    ("M1171-X-PROVENANCE", "provenance_boundary", "Resolve terminal declarations, bodies, revisions, licenses, axioms, and transitive TCB.", "Transitive provenance and trust closure", "No anchor-only candidate is mistaken for a proof body.", "critical", "not_applicable", "M4"),
]

PROOF_EDGES = [
    ("M1171-T-ASSEMBLE", ROOT),
    ("M1171-S-DEFINITIONS", "M1171-T-ASSEMBLE"),
    ("M1171-S-BOUNDARIES", "M1171-T-ASSEMBLE"),
    ("M1171-S-FOUNDATION", "M1171-T-ASSEMBLE"),
    ("M1171-T-COMPONENT", "M1171-T-ASSEMBLE"),
    ("M1171-L-FDERIV-PARTIAL", "M1171-T-ASSEMBLE"),
    ("M1171-L-TRACE", "M1171-T-ASSEMBLE"),
    ("M1171-L-OPNORM", "M1171-T-ASSEMBLE"),
    ("M1171-L-LP-ASSEMBLY", "M1171-T-ASSEMBLE"),
    ("M1171-N-SCHWARTZ", "M1171-T-COMPONENT"),
    ("M1171-N-COMPLEX", "M1171-T-COMPONENT"),
    ("M1171-L-FOURIER-DERIV", "M1171-T-COMPONENT"),
    ("M1171-C-MULTIPLIER", "M1171-T-COMPONENT"),
    ("M1171-L-MIHLIN", "M1171-T-COMPONENT"),
    ("M1171-L-ZERO-FREQ", "M1171-T-COMPONENT"),
]


def fingerprint(oid: str, target: str) -> str:
    if oid == ROOT:
        return "lean-expression-sha256:94cb9c63c1ee16182bd550388d2f29156c59a6a5cbda91509fead48fcfcc2fd8"
    return "planned:v1:sha256:" + hashlib.sha256(target.encode()).hexdigest()


def edge_graph(name: str, pairs: list[tuple[str, str]]) -> dict:
    edges = []
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for index, (source, target) in enumerate(pairs, 1):
        edge_id = f"{name.upper()}-{index:02d}"
        edges.append({"edge_id": edge_id, "from": source, "to": target})
        outgoing.setdefault(source, []).append(edge_id)
        incoming.setdefault(target, []).append(edge_id)
    return {"edges": edges, "in": incoming, "out": outgoing}


def main() -> None:
    ids = [row[0] for row in SPECS]
    informational = ["M1171-X-SOURCE", "M1171-X-PROVENANCE"]
    obligations = []
    nodes = []
    for oid, kind, statement, target, output, risk, human, machine in SPECS:
        machine_eligibility = "informational" if oid in informational else "required"
        human_eligibility = "not_applicable" if human == "not_applicable" else "required"
        obligations.append({
            "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target),
            "kind": kind, "root_relevant": oid not in informational,
            "machine_eligibility": machine_eligibility,
            "human_source_eligibility": human_eligibility,
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "typed source/provenance overlay; no semantic proof credit" if oid in informational else None,
            "terminal_proof_body_id": None,
        })
        leaf = oid not in {target_id for _, target_id in PROOF_EDGES}
        ledger = [
            "Freeze the exact hypotheses and named input interfaces.",
            f"Establish the stated transition: {statement}",
            f"Derive the declared output: {output}",
            "Pass that output to the parent edge without strengthening or changing the target.",
        ] if leaf else ["Consume every required incoming proof edge.", f"Derive: {output}", "Record an exact child-to-parent composition certificate."]
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind,
            "human_statement": statement, "formal_target": target, "output": output,
            "human_debt": human, "machine_debt": machine, "readability_debt": "R4",
            "evidence_ids": [], "source_crosswalk_id": "pending-node-pinpoint-review",
            "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
            "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
            "step_budget": len(ledger), "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-1171/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": f"VAL-{oid}-PENDING",
            "status_boundary": "Architecture only; this planned interface is not a theorem declaration or proof body.",
            "task_ids": [ITEM, "S56-M-1171-PROOF"], "owned_sources": [],
            "owner": "THM-M-1171 proof implementer", "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
        })

    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
        "theorem_id": "THM-M-1171", "registry_version": 1,
        "freeze_basis": "Exact statement plus the bounded anchor audit, with closure status ignored while the Fourier-multiplier architecture and eligibility were selected.",
        "root_obligation_id": ROOT,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": informational,
        },
        "eligibility_policy": "Semantic proof obligations are required independently of availability. Source and provenance overlays cannot earn proof credit.",
        "exclusions": [
            "Weak (1,1), endpoint, weighted, bounded-domain, variable-coefficient, vector-valued, or parabolic estimates are not the root.",
            "Aliases, definitional expansions, wrappers, and component presentation splits do not create distinct proof-body credit.",
            "The external Carleson weak (1,1) theorem is related discovery evidence only and is not an eligible terminal body for this root.",
        ],
        "obligations": obligations,
        "closure_observed_after_freeze": False,
        "status_boundary": "The registry freezes planned obligations only; no obligation is closed and theorem_complete is false.",
    }
    canonical = json.dumps(registry["frozen_denominators"], sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()

    refinement = [("M1171-S-DEFINITIONS", ROOT), ("M1171-S-BOUNDARIES", ROOT)]
    provenance = [("M1171-X-PROVENANCE", oid) for oid in ids if oid not in informational]
    evidence = [(oid, ROOT) for oid in ["M1171-S-DEFINITIONS", "M1171-X-SOURCE", "M1171-X-PROVENANCE"]]
    trust = [("M1171-S-FOUNDATION", ROOT), ("M1171-X-PROVENANCE", "M1171-S-FOUNDATION")]
    documentation = [(oid, ROOT) for oid in ids if oid != ROOT]
    workflow = [("M1171-X-SOURCE", "M1171-X-PROVENANCE"), ("M1171-X-PROVENANCE", "M1171-S-FOUNDATION"), ("M1171-T-COMPONENT", "M1171-T-ASSEMBLE"), ("M1171-T-ASSEMBLE", ROOT)]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1171",
        "registry_id": "THM-M-1171/registry-v1", "registry_denominator_sha256": digest,
        "root_node_id": ROOT, "edge_direction": "prerequisite_or_child -> consumer_or_parent",
        "nodes": nodes,
        "graphs": {name: edge_graph(name, pairs) for name, pairs in [
            ("proof", PROOF_EDGES), ("refinement", refinement), ("provenance", provenance),
            ("evidence", evidence), ("trust", trust), ("documentation", documentation), ("workflow", workflow)]},
        "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False,
                             "theorem_complete": False,
                             "remaining_root_cut_set": ["M1171-L-MIHLIN", "M1171-L-FOURIER-DERIV", "M1171-L-LP-ASSEMBLY"],
                             "root_machine_debt": "M4"},
    }
    (HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    (HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

    lines = ["# THM-M-1171 obligation tree", "", "The frozen proof route is Fourier-multiplier based. Every entry below is an open architecture obligation, not a proof claim.", ""]
    children: dict[str, list[str]] = {}
    for child, parent in PROOF_EDGES:
        children.setdefault(parent, []).append(child)
    by_id = {row[0]: row for row in SPECS}
    def render(oid: str, depth: int = 0) -> None:
        row = by_id[oid]
        lines.extend([f"{'  ' * depth}- **{oid}** ({row[1]}): {row[2]}", f"{'  ' * depth}  Output: {row[4]}"])
        for child in children.get(oid, []):
            render(child, depth + 1)
    render(ROOT)
    lines += ["", "## Node ledgers", ""]
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for oid in ids:
        node = node_by_id[oid]
        lines += [f"### {oid}", "", node["human_statement"], "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"]
        lines += [f"{index}. {step}" for index, step in enumerate(node["semantic_step_ledger"], 1)]
        lines += [""]
    lines += ["## Typed overlays", "", "`X-SOURCE` and `X-PROVENANCE` cover source and terminal-body boundaries. They are informational overlays and cannot close a proof node or increase a machine denominator.", "", "## Closure boundary", "", "All 16 semantic machine obligations are open. The first critical cut contains `M1171-L-MIHLIN`, `M1171-L-FOURIER-DERIV`, and `M1171-L-LP-ASSEMBLY`. No composition certificate, proof body, H0/R0 review, or theorem completion is claimed.", ""]
    (HERE / "obligation-tree.md").write_text("\n".join(lines))
    print(f"wrote 18 obligations; denominator sha256 {digest}")


if __name__ == "__main__":
    main()
