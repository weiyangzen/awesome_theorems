#!/usr/bin/env python3
"""Generate the frozen THM-M-1200 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1200-OBLIGATION_TREE"
ROOT = "M1200-ROOT"

SPECS = [
    (ROOT, "root", "The exact frozen scalar Rankine-Hugoniot equivalence.", "Stage1Instances.THM_M_1200.RankineHugoniotTarget", "The canonical target.", "critical", "H3", "M4"),
    ("M1200-S-DEFINITIONS", "definition", "Fix the jump coefficient, interface defect, test-function class, domains, and binder order.", "Definitions in Statement.lean", "The exact objects used by both implications.", "high", "not_applicable", "M0-L"),
    ("M1200-S-BOUNDARIES", "normalization", "Retain equal states, stationary interfaces, arbitrary real flux, and every smooth compactly supported spacetime test function.", "Canonical boundary package", "No excluded degenerate case or strengthened regularity premise.", "high", "H3", "M4"),
    ("M1200-S-FOUNDATION", "certificate", "Freeze the classical-analysis, integration, computation, and TCB policy.", "Foundation and trust certificate", "An accepted policy for every terminal body.", "critical", "not_applicable", "M4"),
    ("M1200-N-UNFOLD", "reduction", "Unfold vanishing defect to a scalar coefficient multiplied by every admissible trace integral.", "InterfaceDefectVanishes f uL uR s", "The quantified product-zero formulation.", "normal", "H3", "M4"),
    ("M1200-B-FORWARD", "branch", "From vanishing against all tests, derive that the jump coefficient is zero.", "InterfaceDefectVanishes f uL uR s -> jumpCoefficient f uL uR s = 0", "Zero interface coefficient.", "critical", "H3", "M4"),
    ("M1200-C-TEST", "construction", "Construct one smooth compactly supported spacetime test function whose interface-trace integral is nonzero.", "NonzeroTracePackage", "An admissible phi with nonzero integral along x = s*t, uniformly for s.", "critical", "H3", "M4"),
    ("M1200-L-TRACE", "core_lemma", "Verify smoothness and compact support of the selected spacetime bump and identify its interface trace.", "ContDiff Real top phi and HasCompactSupport phi", "Admissibility plus the pointwise trace formula.", "high", "H3", "M4"),
    ("M1200-L-INTEGRAL", "core_lemma", "Prove the selected interface trace has a strictly positive, hence nonzero, Lebesgue integral.", "integral (fun t => phi (t, s*t)) != 0", "A cancellable scalar test integral.", "critical", "H3", "M4"),
    ("M1200-B-REVERSE", "branch", "From the jump equality, show every admissible interface defect is zero.", "s * (uR-uL) = f uR-f uL -> InterfaceDefectVanishes f uL uR s", "The reverse implication for arbitrary tests.", "normal", "H3", "M4"),
    ("M1200-L-ALGEBRA", "core_lemma", "Transport between zero jump coefficient and the canonical Rankine-Hugoniot equality.", "jumpCoefficient f uL uR s = 0 <-> s*(uR-uL)=f uR-f uL", "The exact sign and equality normalization.", "high", "H3", "M4"),
    ("M1200-T-ASSEMBLE", "transport", "Compose the two implications and coefficient normalization into the exact root equivalence.", "NonzeroTracePackage -> RankineHugoniotTarget", "The exact root, conditional only on the explicit construction package.", "critical", "H3", "M4"),
    ("M1200-X-SOURCE", "terminal", "Pinpoint primary sources for the weak-interface reduction, bump argument, and algebraic jump law.", "Reviewed node-specific source crosswalk", "Human-source evidence only.", "high", "H3", "not_applicable"),
    ("M1200-X-PROVENANCE", "terminal", "Resolve terminal bodies, revisions, licenses, axioms, and transitive trust closure.", "Transitive provenance record", "No supporting import is mistaken for root closure.", "critical", "not_applicable", "M4"),
]

# Parent -> required child. Reciprocal typed edges are emitted for every relation.
PROOF_REQUIRES = [
    (ROOT, "M1200-T-ASSEMBLE"),
    ("M1200-T-ASSEMBLE", "M1200-S-DEFINITIONS"),
    ("M1200-T-ASSEMBLE", "M1200-S-BOUNDARIES"),
    ("M1200-T-ASSEMBLE", "M1200-N-UNFOLD"),
    ("M1200-T-ASSEMBLE", "M1200-B-FORWARD"),
    ("M1200-T-ASSEMBLE", "M1200-B-REVERSE"),
    ("M1200-T-ASSEMBLE", "M1200-L-ALGEBRA"),
    ("M1200-B-FORWARD", "M1200-C-TEST"),
    ("M1200-C-TEST", "M1200-L-TRACE"),
    ("M1200-C-TEST", "M1200-L-INTEGRAL"),
]


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def graph(name: str, triples: list[tuple[str, str, str]]) -> dict:
    edges, incoming, outgoing = [], {}, {}
    for i, (source, target, edge_type) in enumerate(triples, 1):
        eid = f"{name.upper()}-{i:02d}"
        edge = {"edge_id": eid, "from": source, "to": target, "type": edge_type}
        edges.append(edge)
        outgoing.setdefault(source, []).append(eid)
        incoming.setdefault(target, []).append(eid)
    return {"edges": edges, "in": incoming, "out": outgoing}


def main() -> None:
    ids = [row[0] for row in SPECS]
    informational = {"M1200-X-SOURCE", "M1200-X-PROVENANCE"}
    obligations, nodes = [], []
    parents = {p for p, _ in PROOF_REQUIRES}
    for oid, kind, statement, target, output, risk, human, machine in SPECS:
        info = oid in informational
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": "lean-expression-sha256:b77d79ed6acc61642c8288a004f1023d65a71367415ac90fd6a6c5e8af77ca93" if oid == ROOT else "planned:v1:sha256:" + sha(target),
            "kind": kind, "root_relevant": not info,
            "machine_eligibility": "informational" if info else "required",
            "human_source_eligibility": "not_applicable" if human == "not_applicable" else "required",
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": "typed source/provenance overlay; no semantic proof credit" if info else None,
            "terminal_proof_body_id": None,
        })
        if oid in parents:
            ledger = {"premises": ["all incoming proof_requires children"], "inference": "checked child-to-parent composition required", "output": output, "outgoing_use": "the unique parent proof edge, or root publication"}
        else:
            ledger = {"premises": ["the exact frozen context and named inputs"], "inference": statement, "output": output, "outgoing_use": "the declared parent proof edge, or non-proof overlay"}
        nodes.append({
            "node_id": oid, "obligation_id": oid, "kind": kind, "human_statement": statement,
            "formal_target": target, "output": output, "human_debt": human, "machine_debt": machine,
            "readability_debt": "R3", "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if human == "not_applicable" else "pending-node-pinpoint-review",
            "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
            "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
            "step_budget": 4 if oid not in parents else 3, "semantic_step_ledger": ledger,
            "public_readable_target": f"Stage1_Instances/THM-M-1200/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": f"VAL-{oid}-PENDING",
            "status_boundary": "Architecture only; no open mathematical premise is discharged by this node record.",
            "task_ids": [ITEM, "S56-M-1200-PROOF"], "owned_sources": [],
            "owner": "THM-M-1200 proof implementer", "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source-map change; revocation=none",
        })

    projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{k: row[k] for k in projection_fields} for row in obligations]
    digest = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1200",
        "registry_version": 1,
        "freeze_basis": "The exact statement and bounded anchor audit were inputs; availability and closure status were not used to select eligibility or the bump-test proof architecture.",
        "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
        "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
        "root_obligation_id": ROOT, "denominator_sha256": digest,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids, "informational_overlays": sorted(informational),
        },
        "eligibility_policy": "All semantic children are required independent of current library availability; source and provenance overlays cannot earn machine proof credit.",
        "exclusions": [
            "Deriving the frozen interface defect from a distributional piecewise-state weak solution is outside the selected reduced theorem and receives no hidden credit.",
            "Entropy admissibility, systems, curved or multidimensional interfaces, balance laws, existence, and uniqueness are not the root.",
            "Aliases, moving-frame wrappers, definition unfolding, and presentation splits cannot create distinct semantic or proof-body credit.",
        ],
        "obligations": obligations, "closure_observed_after_freeze": False,
        "status_boundary": "This freezes an open architecture. No new proof body, H0/R0 review, root closure, or theorem completion is claimed.",
    }

    proof_triples = []
    for i, (parent, child) in enumerate(PROOF_REQUIRES, 1):
        req, comp = f"PROOF-{2*i-1:02d}", f"PROOF-{2*i:02d}"
        proof_triples.extend([(parent, child, "proof_requires", req, comp), (child, parent, "composes", comp, req)])
    proof_edges, pin, pout = [], {}, {}
    for source, target, typ, eid, reciprocal in proof_triples:
        proof_edges.append({"edge_id": eid, "from": source, "to": target, "type": typ, "reciprocal_edge_id": reciprocal})
        pout.setdefault(source, []).append(eid); pin.setdefault(target, []).append(eid)

    overlays = {
        "refinement": [("M1200-S-DEFINITIONS", ROOT, "logical_decomposition"), ("M1200-S-BOUNDARIES", ROOT, "logical_decomposition")],
        "provenance": [("M1200-X-PROVENANCE", oid, "provenance_of") for oid in ids if oid not in informational],
        "evidence": [("M1200-X-SOURCE", ROOT, "evidence_for"), ("M1200-X-PROVENANCE", ROOT, "evidence_for")],
        "trust": [("M1200-S-FOUNDATION", ROOT, "trusts"), ("M1200-X-PROVENANCE", "M1200-S-FOUNDATION", "trusts")],
        "documentation": [(oid, ROOT, "documents") for oid in ids if oid != ROOT],
        "workflow": [("M1200-X-SOURCE", "M1200-X-PROVENANCE", "workflow_depends_on"), ("M1200-C-TEST", "M1200-B-FORWARD", "workflow_depends_on"), ("M1200-T-ASSEMBLE", ROOT, "workflow_depends_on")],
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1200",
        "registry_id": "THM-M-1200/registry-v1", "registry_denominator_sha256": digest,
        "root_node_id": ROOT, "edge_direction": "typed; proof_requires is parent-to-child and composes is reciprocal child-to-parent",
        "nodes": nodes, "graphs": {"proof": {"edges": proof_edges, "in": pin, "out": pout}, **{name: graph(name, triples) for name, triples in overlays.items()}},
        "closure_boundary": {"closed_obligations": ["M1200-S-DEFINITIONS"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1200-C-TEST"], "root_machine_debt": "M4"},
    }
    (HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    (HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

    by_id = {row[0]: row for row in SPECS}
    children = {}
    for parent, child in PROOF_REQUIRES: children.setdefault(parent, []).append(child)
    lines = ["# THM-M-1200 obligation tree", "", "The frozen route uses one nonzero smooth compactly supported interface trace to cancel the scalar jump coefficient. Nodes remain open unless explicitly kernel-backed; this architecture is not a proof claim.", ""]
    def render(oid: str, depth: int = 0) -> None:
        row = by_id[oid]
        lines.extend([f"{'  '*depth}- **{oid}** ({row[1]}): {row[2]}", f"{'  '*depth}  Output: {row[4]}"])
        for child in children.get(oid, []): render(child, depth + 1)
    render(ROOT)
    lines += ["", "## Node ledgers", ""]
    node_map = {n["obligation_id"]: n for n in nodes}
    for oid in ids:
        n = node_map[oid]
        lines += [f"### {oid}", "", n["human_statement"], "", f"Formal target: `{n['formal_target']}`", "", f"Output: {n['output']}", "", "Semantic ledger:", f"1. Premises: {', '.join(n['semantic_step_ledger']['premises'])}.", f"2. Inference: {n['semantic_step_ledger']['inference']}.", f"3. Output: {n['semantic_step_ledger']['output']}.", f"4. Outgoing use: {n['semantic_step_ledger']['outgoing_use']}.", ""]
    lines += ["## Closure boundary", "", "The only kernel-backed registry node is the previously frozen definition surface. The critical open cut is `M1200-C-TEST`; its trace-admissibility and nonzero-integral children must be implemented before the forward branch can close. The checked conditional composition consumes this package explicitly and gives it no closure credit. Source review, provenance/trust closure, readable review, validation, release, and theorem completion remain open.", ""]
    (HERE / "obligation-tree.md").write_text("\n".join(lines))
    print(f"generated {len(ids)} obligations; denominator {digest}")


if __name__ == "__main__":
    main()
