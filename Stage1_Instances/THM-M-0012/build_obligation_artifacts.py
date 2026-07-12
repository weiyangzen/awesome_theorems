#!/usr/bin/env python3
"""Build the frozen THM-M-0012 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0012-OBLIGATION_TREE"
THEOREM = "THM-M-0012"
PREFIX = "M0012-"
ROOT_EXPRESSION = "d14207f425a984b6daefaa986d8351a1543f58b7631d1c842e51a3ef2392ba74"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# short id, kind, risk, human statement, formal target, output, machine eligibility,
# human-source eligibility, terminal proof-body identity, step budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "Every nonconstant univariate complex polynomial has a complex root.",
        "Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget",
        "The exact frozen pointwise fundamental-theorem-of-algebra proposition.",
        "required", "required", None, 12,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Freeze f : Polynomial Complex, exclusion of every C c, and an existential Complex IsRoot conclusion in their exact binder order.",
        "Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget",
        "The exact domain, antecedent, existential witness, and root predicate.",
        "required", "not_applicable", None, 12,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Exclude zero and all constants while retaining X, all linear polynomials, and all higher positive-degree polynomials.",
        "zero_not_nonconstant; C_not_nonconstant; X_nonconstant",
        "The exact degenerate and linear boundary policy.",
        "required", "not_applicable", None, 16,
    ),
    (
        "S-ENCODINGS", "transport", "high",
        "Relate the canonical target bidirectionally to positive-degree root existence and evaluation-at-zero without crediting algebraic closedness as a second proof.",
        "fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget; fundamentalTheoremOfAlgebraTarget_iff_evaluationRootTarget",
        "Two checked iff transports and one explicit deduplication boundary.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0012.fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget", 18,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Fix the Lean kernel, classical logic, quotient, extensionality, computation, and no-oracle policy for the proof route.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation and computation boundary.",
        "required", "not_applicable", None, 30,
    ),
    (
        "N-DEGREE", "normalization", "high",
        "Convert exclusion of every constant polynomial to positive WithBot Nat degree.",
        "Stage1Instances.THM_M_0012.nonconstant_iff_degree_pos",
        "Nonconstant f implies 0 < degree f for the anchor interface.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0012.nonconstant_iff_degree_pos", 24,
    ),
    (
        "A-POSITIVE-ROOT", "bridge", "critical",
        "Every positive-degree complex polynomial has a complex root.",
        "Complex.exists_root",
        "The exact positive-degree root package consumed by root composition.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Complex.exists_root", 20,
    ),
    (
        "B-NO-ROOT", "branch", "critical",
        "Assuming positive degree and no root, derive False; then recompose the contradiction into root existence.",
        "Stage1Instances.THM_M_0012.ObligationTree.NoRootContradictionEngine",
        "The exhaustive root-free contradiction branch.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0012.ObligationTree.positiveDegreeAnchor_of_noRootContradiction", 32,
    ),
    (
        "C-RECIPROCAL", "construction", "normal",
        "Construct the total function z maps to (f.eval z)^-1; under root-freeness its denominator is pointwise nonzero.",
        "fun z : Complex => (Polynomial.eval z f)⁻¹",
        "The reciprocal-evaluation function and its nonzero invariant.",
        "not_applicable", "required", None, 16,
    ),
    (
        "L-RECIPROCAL-DIFF", "core_lemma", "critical",
        "Polynomial evaluation is differentiable and the inverse of a pointwise nonzero differentiable function is differentiable.",
        "Polynomial.differentiable; Differentiable.inv",
        "Differentiability of z maps to (f.eval z)^-1 under root-freeness.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Polynomial.differentiable+Differentiable.inv", 36,
    ),
    (
        "L-RECIPROCAL-DECAY", "core_lemma", "critical",
        "Positive-degree polynomial norm tends to infinity, so inverse evaluation tends to zero along the complex cocompact filter.",
        "Polynomial.tendsto_norm_atTop; Filter.tendsto_inv₀_cobounded",
        "Tendsto reciprocal evaluation (cocompact Complex) (nhds 0).",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Polynomial.tendsto_norm_atTop+Filter.tendsto_inv₀_cobounded", 48,
    ),
    (
        "L-LIOUVILLE", "bridge", "critical",
        "A differentiable complex function tending to zero at infinity is pointwise zero.",
        "Differentiable.apply_eq_of_tendsto_cocompact",
        "For every z, (f.eval z)^-1 = 0.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Differentiable.apply_eq_of_tendsto_cocompact", 30,
    ),
    (
        "L-POLYNOMIAL-CONSTANT", "core_lemma", "critical",
        "Pointwise zero inverse evaluations imply f = C 0 by inverse injectivity and polynomial extensionality.",
        "inv_injective; Polynomial.funext",
        "f = Polynomial.C 0, contradicting positive degree.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:inv_injective+Polynomial.funext", 32,
    ),
    (
        "T-ANALYTIC-COMPOSE", "terminal", "critical",
        "Consume all four analytic engines to close the root-free contradiction without invoking Complex.exists_root.",
        "Stage1Instances.THM_M_0012.ObligationTree.noRootContradiction_of_engines",
        "NoRootContradictionEngine from differentiability, decay, Liouville, and polynomial identity.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0012.ObligationTree.noRootContradiction_of_engines", 28,
    ),
    (
        "T-ROOT-COMPOSE", "terminal", "critical",
        "Consume the nonconstant-to-degree bridge and positive-degree anchor to yield the exact frozen root.",
        "Stage1Instances.THM_M_0012.ObligationTree.root_of_degreeBridge_and_positiveDegreeAnchor",
        "The exact root conditional on both explicit children.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0012.ObligationTree.root_of_degreeBridge_and_positiveDegreeAnchor", 18,
    ),
    (
        "X-SOURCE", "source_boundary", "high",
        "Pinpoint and independently review a primary proof, assumptions, historical wording, and errata for every mathematical node.",
        "primary-source packet and independent review pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", None, 40,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Audit the exact terminal body, aliases, wrapper identity, source blobs, imported declarations, revisions, and licenses.",
        "Complex.exists_root at pinned mathlib plus its transitive declarations",
        "Body-level provenance without duplicate proof credit.",
        "informational", "not_applicable", None, 45,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit Lean, mathlib, axioms, compiled artifacts, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0; mathlib 8a178386; transitive closure pending",
        "Release-grade trust inventory without mathematical proof credit.",
        "informational", "not_applicable", None, 45,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a complete readable reconstruction of the Liouville proof route.",
        "node-specific readable reconstruction pending",
        "Readable coverage and reviewer decision without machine proof credit.",
        "not_applicable", "required", None, 60,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
        "Stage1 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 24,
    ),
)


CHECKED_INTERFACES = {
    oid("S-INTERFACE"),
    oid("S-BOUNDARY"),
    oid("S-ENCODINGS"),
    oid("N-DEGREE"),
    oid("T-ANALYTIC-COMPOSE"),
    oid("T-ROOT-COMPOSE"),
}
SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-ENCODINGS"),
    oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW"),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusion_reasons = {
        oid("S-INTERFACE"): "formal_statement_interface_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-BOUNDARY"): "formal_boundary_fixture_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-ENCODINGS"): "formal_encoding_transport_human_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
        oid("C-RECIPROCAL"): "definitionally_total_construction_has_no_separate_machine_premise_pending_reviewer_acceptance",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }

    for short, kind, risk, claim, target, output, machine, human_source, body, budget in ROWS:
        identifier = oid(short)
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest(
                [identifier, kind, claim, target, output]
            )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": identifier not in {
                    oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")
                },
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": "required",
                "risk_class": risk,
                "exclusion_reason": exclusion_reasons.get(identifier),
                "terminal_proof_body_id": body,
            }
        )

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier == oid("A-POSITIVE-ROOT"):
            machine_debt = "M0-W"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("A-POSITIVE-ROOT"):
            provenance = "anchor-audit:M0012-C01-MATHLIB-DIRECT"
        elif identifier == oid("L-LIOUVILLE"):
            provenance = "pinned-mathlib:Differentiable.apply_eq_of_tendsto_cocompact"
        elif identifier in {oid("T-ANALYTIC-COMPOSE"), oid("T-ROOT-COMPOSE")}:
            provenance = "local-conditional-composition"
        elif short.startswith(("L-", "N-")):
            provenance = "pinned-visible-terminal-chain"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {oid("T-ANALYTIC-COMPOSE"), oid("T-ROOT-COMPOSE")}:
            owned_sources = ["Stage1_Instances/THM-M-0012/ObligationTree.lean"]
        elif identifier in {oid("S-ENCODINGS"), oid("N-DEGREE")}:
            owned_sources = ["Stage1_Instances/THM-M-0012/Statement.lean"]

        nodes.append(
            {
                "node_id": f"{THEOREM}-{short}",
                "obligation_id": identifier,
                "kind": kind,
                "human_statement": claim,
                "formal_target": target,
                "output": output,
                "human_debt": "H1",
                "machine_debt": machine_debt,
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "not-applicable-pending-review"
                    if identifier in SOURCE_NA else "primary-source-node-map-pending"
                ),
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
                "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
                "step_budget": budget,
                "semantic_step_ledger": {
                    "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                    "inference": target,
                    "output": output,
                    "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0012/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": f"VAL-{identifier}",
                "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
                "task_ids": [ITEM, "S56-M-0012-PROOF"],
                "owned_sources": owned_sources,
                "owner": "THM-M-0012 proof lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": [
                        "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                        "typed-graphs.json", "toolchain and dependency pins",
                    ],
                    "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
                },
            }
        )

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0012-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact frozen statement and visible semantic architecture of the pinned Complex.exists_root body. Eligibility and denominators are fixed independently of candidate closure credit.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "symmetry_and_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The target and terminal proof use no symmetry, sign, ordering, representative, or local/global normalization beyond the explicit nonconstant-to-positive-degree node.",
            },
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The visible terminal body has one exhaustive root-free contradiction branch; constant and linear boundaries are retained in S-BOUNDARY rather than removed.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, numerical approximation, native code, oracle, experiment, or finite certificate participates in the visible route.",
            },
        },
        "proof_body_aliases": {
            "Complex.isAlgClosed": "deduplicated_to:Complex.exists_root",
            "IsAlgClosed.exists_root_for_Complex": "deduplicated_to:Complex.exists_root_via_Complex.isAlgClosed",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("A-POSITIVE-ROOT"),
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact candidate is not installed or accepted; H0, R0, audit completion, validation, release, and theorem completion remain open.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = {
        oid("ROOT"): [oid("T-ROOT-COMPOSE")],
        oid("T-ROOT-COMPOSE"): [oid("N-DEGREE"), oid("A-POSITIVE-ROOT")],
        oid("A-POSITIVE-ROOT"): [oid("B-NO-ROOT")],
        oid("B-NO-ROOT"): [oid("T-ANALYTIC-COMPOSE")],
        oid("T-ANALYTIC-COMPOSE"): [
            oid("L-RECIPROCAL-DIFF"), oid("L-RECIPROCAL-DECAY"),
            oid("L-LIOUVILLE"), oid("L-POLYNOMIAL-CONSTANT"),
        ],
    }
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            requirement = f"REQ-{parent}-{child}"
            composition = f"CMP-{child}-{parent}"
            proof.extend(
                [
                    edge(requirement, parent, "proof_requires", child, composition),
                    edge(composition, child, "composes", parent, requirement),
                ]
            )

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-ENCODINGS", oid("ROOT"), "transports", oid("S-ENCODINGS")),
            edge("REF-BRANCH-RECIPROCAL", oid("B-NO-ROOT"), "expository_decomposition", oid("C-RECIPROCAL")),
            edge("REF-BRANCH-COMPOSE", oid("B-NO-ROOT"), "logical_decomposition", oid("T-ANALYTIC-COMPOSE")),
        ],
        "provenance": [
            edge("PROV-ANCHOR", oid("X-PROVENANCE"), "provenance_of", oid("A-POSITIVE-ROOT")),
            edge("PROV-LIOUVILLE", oid("X-PROVENANCE"), "provenance_of", oid("L-LIOUVILLE")),
            edge("PROV-DECAY", oid("X-PROVENANCE"), "provenance_of", oid("L-RECIPROCAL-DECAY")),
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-ANALYTIC", oid("X-SOURCE"), "source_map", oid("T-ANALYTIC-COMPOSE")),
        ],
        "evidence": [
            edge("EVID-PROVENANCE-ANCHOR", oid("X-PROVENANCE"), "evidence_for", oid("A-POSITIVE-ROOT")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-ANCHOR-CLOSURE", oid("A-POSITIVE-ROOT"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-ANALYTIC", oid("X-READABLE"), "documents", oid("T-ANALYTIC-COMPOSE")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-ROOT-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("A-POSITIVE-ROOT")),
            edge("FLOW-ROOT-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-ROOT-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-ROOT-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-ROOT-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
        ],
    }
    graphs = {}
    for name in GRAPH_NAMES:
        outgoing = {identifier: [] for identifier in ids}
        incoming = {identifier: [] for identifier in ids}
        for row in graph_edges[name]:
            outgoing[row["from"]].append(row["edge_id"])
            incoming[row["to"]].append(row["edge_id"])
        graphs[name] = {"edges": graph_edges[name], "out": outgoing, "in": incoming}

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0012-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_only_obligations": [oid("A-POSITIVE-ROOT")],
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("A-POSITIVE-ROOT"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0012.ObligationTree.noRootContradiction_of_engines",
                "Stage1Instances.THM_M_0012.ObligationTree.positiveDegreeAnchor_of_noRootContradiction",
                "Stage1Instances.THM_M_0012.ObligationTree.root_of_degreeBridge_and_positiveDegreeAnchor",
            ],
            "reason": "Every composition is conditional; the exact pinned anchor remains uninstalled and unaccepted until proof-phase and master validation.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [],
    }
    declaration_map = {
        oid("A-POSITIVE-ROOT"): ["Complex.exists_root"],
        oid("L-LIOUVILLE"): ["Differentiable.apply_eq_of_tendsto_cocompact"],
        oid("T-ANALYTIC-COMPOSE"): ["Stage1Instances.THM_M_0012.ObligationTree.noRootContradiction_of_engines"],
        oid("T-ROOT-COMPOSE"): ["Stage1Instances.THM_M_0012.ObligationTree.root_of_degreeBridge_and_positiveDegreeAnchor"],
    }
    for identifier in ids:
        recipes["recipes"].append(
            {
                "recipe_id": f"VAL-{identifier}",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0012/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0012 obligation tree",
                    }
                ],
                "covered_obligation_ids": [identifier],
                "covered_declarations": declaration_map.get(identifier, []),
            }
        )
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(
        ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
