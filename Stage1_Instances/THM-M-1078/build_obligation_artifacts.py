#!/usr/bin/env python3
"""Build the frozen THM-M-1078 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1078-OBLIGATION_TREE"
THEOREM = "THM-M-1078"
ROOT = "M1078-ROOT"

# Selected before inspecting closure: integrate the audited Burkholder candidate through explicit
# compatibility bridges, then discharge the one genuinely stronger all-time MemLp premise.
SPECS = [
    (ROOT, "root", "The exact frozen finite-horizon martingale-transform inequality.", "Stage1Instances.THM_M_1078.MartingaleTransformTarget", "The canonical target.", "critical", "H2", "M2"),
    ("M1078-S-TARGET", "definition", "Freeze the transform, exponent, constant, binders, and terminal norm conclusion.", "Statement.lean target_iff_expandedSourceShape", "The exact interface consumed at the root.", "high", "not_applicable", "M3"),
    ("M1078-S-BOUNDARY", "normalization", "Retain pointwise multiplier bounds, horizon zero, and excluded endpoint exponents.", "Boundary package for MartingaleTransformTarget", "No endpoint, maximal, square-function, or continuous-time substitute.", "high", "H2", "M4"),
    ("M1078-S-FOUNDATION", "certificate", "Freeze classical noncomputable measure theory and the transitive Lean/mathlib trust boundary.", "Foundation and TCB certificate", "A reviewed trust profile for every eventual body.", "critical", "not_applicable", "M4"),
    ("M1078-C-EXTERNAL-PIN", "integration", "Vendor or pin the audited SmaniaD/Burkholder body at its immutable revision in a compatible dependency closure.", "MeasureTheory.Lp_Burkholder_inequality_martingaleTransform at afa97ef3c85697fa3b2a67af89af8d6dd09eda69", "A locally kernel-checked candidate body, not an upstream badge.", "critical", "H2", "M2"),
    ("M1078-B-INDEX", "transport", "Remove the external initial term and align its inclusive range with increments 1 through n.", "External martingaleTransform indexing -> Stage1 martingaleTransform", "Exact equality of the two transform functions for the chosen zero initial coefficient.", "critical", "H2", "M4"),
    ("M1078-B-PREDICTABLE", "transport", "Bridge mathlib IsPredictable to the external IsStronglyPredictable interface with the required shift.", "IsPredictable F v -> external strongly predictable coefficient process", "The external measurability premise without strengthening the root.", "critical", "H2", "M4"),
    ("M1078-B-BOUND", "transport", "Convert the frozen pointwise absolute-value bound to the external almost-everywhere coefficient bound.", "(forall k omega, abs (v k omega) <= 1) -> external ae bound", "The candidate multiplier-bound premise.", "high", "H2", "M4"),
    ("M1078-B-FINITE", "instance_bridge", "Expose finiteness of the measure from the probability-measure instance.", "IsProbabilityMeasure mu -> IsFiniteMeasure mu", "The external finite-measure instance.", "medium", "H2", "M3"),
    ("M1078-B-NORM", "transport", "Convert the candidate eLpNorm/ENNReal inequality and explicit constant to the frozen lpNorm/Real inequality.", "external eLpNorm conclusion -> lpNorm conclusion", "A finite nonnegative real constant depending only on p.", "critical", "H2", "M4"),
    ("M1078-T-ALLTIME", "bridge", "Derive MemLp at every earlier time from terminal MemLp for a real martingale.", "Martingale f F mu -> MemLp (f n) p mu -> forall k <= n, MemLp (f k) p mu", "The extra all-time integrability premise required by the candidate route.", "critical", "H2", "M4"),
    ("M1078-T-LOCAL-BODY", "composition", "Compose the pinned theorem with indexing, predictability, bound, finiteness, and norm transports.", "AllTimeMemLpTransformBound", "The frozen inequality under an explicit all-time MemLp premise.", "critical", "H2", "M4"),
    ("M1078-T-ASSEMBLE", "composition", "Apply the all-time integrability bridge to the local integrated body.", "root_of_allTimeMemLpTransformBound", "The exact canonical target.", "critical", "H2", "M4"),
    ("M1078-X-SOURCE", "source_boundary", "Pinpoint primary statements for the transform inequality and every material bridge, including errata.", "Reviewed node-specific source crosswalk", "Human-source evidence without machine-proof credit.", "high", "H2", "not_applicable"),
    ("M1078-X-PROVENANCE", "provenance_boundary", "Resolve the external terminal body, transitive declarations, licenses, axioms, and TCB.", "Transitive provenance and trust closure", "No near match or upstream build badge is treated as local closure.", "critical", "not_applicable", "M2"),
]

PROOF_EDGES = [
    ("M1078-T-ASSEMBLE", ROOT),
    ("M1078-S-TARGET", "M1078-T-ASSEMBLE"),
    ("M1078-S-BOUNDARY", "M1078-T-ASSEMBLE"),
    ("M1078-S-FOUNDATION", "M1078-T-ASSEMBLE"),
    ("M1078-T-ALLTIME", "M1078-T-ASSEMBLE"),
    ("M1078-T-LOCAL-BODY", "M1078-T-ASSEMBLE"),
    ("M1078-C-EXTERNAL-PIN", "M1078-T-LOCAL-BODY"),
    ("M1078-B-INDEX", "M1078-T-LOCAL-BODY"),
    ("M1078-B-PREDICTABLE", "M1078-T-LOCAL-BODY"),
    ("M1078-B-BOUND", "M1078-T-LOCAL-BODY"),
    ("M1078-B-FINITE", "M1078-T-LOCAL-BODY"),
    ("M1078-B-NORM", "M1078-T-LOCAL-BODY"),
]


def fingerprint(oid: str, target: str) -> str:
    if oid == ROOT:
        return "lean-expression-sha256:675f66dd17fc5f438fc69d579af60f3784063f985924f2c2b059945a7f038aa8"
    return "planned:v1:sha256:" + hashlib.sha256(target.encode()).hexdigest()


def edge_graph(name: str, pairs: list[tuple[str, str]]) -> dict:
    edges, incoming, outgoing = [], {}, {}
    for index, (source, target) in enumerate(pairs, 1):
        edge_id = f"{name.upper()}-{index:02d}"
        edges.append({"edge_id": edge_id, "from": source, "to": target})
        outgoing.setdefault(source, []).append(edge_id)
        incoming.setdefault(target, []).append(edge_id)
    return {"edges": edges, "in": incoming, "out": outgoing}


def main() -> None:
    ids = [row[0] for row in SPECS]
    informational = ["M1078-X-SOURCE", "M1078-X-PROVENANCE"]
    parent_ids = {parent for _, parent in PROOF_EDGES}
    obligations, nodes = [], []
    for oid, kind, statement, target, output, risk, human, machine in SPECS:
        overlay = oid in informational
        obligations.append({
            "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target),
            "kind": kind, "root_relevant": not overlay,
            "machine_eligibility": "informational" if overlay else "required",
            "human_source_eligibility": "not_applicable" if human == "not_applicable" else "required",
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "typed source/provenance overlay; no semantic proof credit" if overlay else None,
            "terminal_proof_body_id": None,
        })
        if oid in parent_ids:
            ledger = ["Consume every registered incoming proof edge at its exact interface.", f"Derive: {output}", "Record checked child-to-parent composition without an undeclared premise."]
        else:
            ledger = ["Freeze the exact hypotheses and named input interfaces.", f"Establish: {statement}", f"Derive: {output}", "Pass the output through its registered typed edge without changing the target."]
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": statement,
            "formal_target": target, "output": output, "human_debt": human,
            "machine_debt": machine, "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "anchor-audit:C03; node-pinpoint-review-pending",
            "provenance_id": "anchor-audit:S56-M-1078-C03" if oid in {"M1078-C-EXTERNAL-PIN", "M1078-X-PROVENANCE"} else "none",
            "foundation_profile": "lean4-dependent-type-theory/classical-measure-theory-audit-pending",
            "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-external-closure-pending",
            "computation_record": "none", "step_budget": len(ledger), "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-1078/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": f"VAL-{oid}-PENDING",
            "status_boundary": "Architecture only; no terminal proof body or obligation closure is credited.",
            "task_ids": [ITEM, "S56-M-1078-PROOF"], "owned_sources": [],
            "owner": "THM-M-1078 proof implementer", "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map,candidate-revision change; revocation=none",
        })

    denominator = {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": informational,
    }
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1,
        "freeze_basis": "Exact elaborated statement plus bounded anchor audit; the audited external-integration route and eligibility were selected without proof-closure credit.",
        "root_obligation_id": ROOT, "frozen_denominators": denominator,
        "eligibility_policy": "Every semantic compatibility bridge remains required regardless of apparent library convenience. Source and provenance overlays earn no proof credit.",
        "exclusions": [
            "BDG maximal/square-function, continuous-time, endpoint, and fixed-p variants are not the root.",
            "The external near match is not an exact wrapper: its indexing, predictability, integrability, norm codomain, and measure-class differences stay explicit.",
            "Aliases, wrappers, transports, source rows, and presentation splits cannot duplicate semantic or terminal-body credit.",
        ],
        "obligations": obligations, "closure_observed_after_freeze": False,
        "status_boundary": "The registry freezes open architecture only; no obligation or theorem is complete.",
    }
    digest = hashlib.sha256(json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    refinement = [("M1078-S-TARGET", ROOT), ("M1078-S-BOUNDARY", ROOT)]
    provenance = [("M1078-X-PROVENANCE", oid) for oid in ids if oid not in informational]
    evidence = [(oid, ROOT) for oid in ["M1078-S-TARGET", "M1078-X-SOURCE", "M1078-X-PROVENANCE"]]
    trust = [("M1078-S-FOUNDATION", ROOT), ("M1078-X-PROVENANCE", "M1078-S-FOUNDATION")]
    documentation = [(oid, ROOT) for oid in ids if oid != ROOT]
    workflow = [("M1078-X-SOURCE", "M1078-X-PROVENANCE"), ("M1078-X-PROVENANCE", "M1078-C-EXTERNAL-PIN"), ("M1078-C-EXTERNAL-PIN", "M1078-T-LOCAL-BODY"), ("M1078-T-LOCAL-BODY", "M1078-T-ASSEMBLE"), ("M1078-T-ASSEMBLE", ROOT)]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1078/registry-v1", "registry_denominator_sha256": digest,
        "statement_source_sha256": "a5412e5aa97c474cf21e6bf35b2daa1dbef36176bea025976456042700915a0e",
        "root_node_id": ROOT, "edge_direction": "prerequisite_or_child -> consumer_or_parent", "nodes": nodes,
        "graphs": {name: edge_graph(name, pairs) for name, pairs in [("proof", PROOF_EDGES), ("refinement", refinement), ("provenance", provenance), ("evidence", evidence), ("trust", trust), ("documentation", documentation), ("workflow", workflow)]},
        "composition_certificates": [{"certificate_id": "COMP-M1078-ROOT-CONDITIONAL", "declaration": "Stage1Instances.THM_M_1078.ObligationTree.root_of_allTimeMemLpTransformBound", "exact_target_transport": "Stage1Instances.THM_M_1078.ObligationTree.local_target_iff_frozen_target", "covered_edges": ["PROOF-01", "PROOF-05", "PROOF-06"], "status": "checked_conditional_composition_only"}],
        "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1078-C-EXTERNAL-PIN", "M1078-T-ALLTIME", "M1078-B-PREDICTABLE", "M1078-B-NORM"], "root_machine_debt": "M2"},
    }
    (HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    (HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

    children = {}
    for child, parent in PROOF_EDGES:
        children.setdefault(parent, []).append(child)
    by_id = {row[0]: row for row in SPECS}
    lines = ["# THM-M-1078 obligation tree", "", "This freezes the audited external-integration route. Every node is open; the tree is architecture, not proof closure.", "", "## Proof route", ""]
    def render(oid: str, depth: int = 0) -> None:
        row = by_id[oid]
        lines.extend([f"{'  ' * depth}- **{oid}** ({row[1]}): {row[2]}", f"{'  ' * depth}  Output: {row[4]}"])
        for child in children.get(oid, []):
            render(child, depth + 1)
    render(ROOT)
    lines.extend(["", "## Node ledgers", ""])
    for node in nodes:
        lines.extend([f"### {node['node_id']}", "", f"Claim: {node['human_statement']}", "", f"Formal target: `{node['formal_target']}`", "", f"Output: {node['output']}", "", "Semantic ledger:"])
        lines.extend([f"{i}. {step}" for i, step in enumerate(node["semantic_step_ledger"], 1)])
        lines.append("")
    lines.extend(["## Typed overlays", "", "The bundle separates proof, refinement, provenance, evidence, trust, documentation, and workflow edges. `X-SOURCE` and `X-PROVENANCE` are informational and cannot increase machine coverage.", "", "## Closure boundary", "", "All 13 semantic machine obligations are open. The first critical cut is `M1078-C-EXTERNAL-PIN`, `M1078-T-ALLTIME`, `M1078-B-PREDICTABLE`, and `M1078-B-NORM`. The checked Lean declaration proves only conditional parent composition. No imported body, exact wrapper, H0/R0 review, audit completion, or theorem completion is claimed.", ""])
    (HERE / "obligation-tree.md").write_text("\n".join(lines))
    print(f"wrote {len(ids)} obligations; denominator sha256 {digest}")


if __name__ == "__main__":
    main()
