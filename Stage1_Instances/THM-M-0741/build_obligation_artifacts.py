#!/usr/bin/env python3
"""Build the frozen THM-M-0741 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0741-OBLIGATION_TREE"
THEOREM = "THM-M-0741"
PREFIX = "M0741-"
ROOT_EXPRESSION = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BLOB = "0834371356762db805d37208b9cf8a1fc0efd217"
MATHLIB_HALTING_BODY = (
    f"mathlib4@{MATHLIB_REVISION}:{MATHLIB_BLOB}"
    "#ComputablePred.halting_problem"
)
MATHLIB_RICE_BODY = (
    f"mathlib4@{MATHLIB_REVISION}:{MATHLIB_BLOB}#ComputablePred.rice"
)
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
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


# short ID, kind, risk, claim, formal target, output, machine eligibility,
# human-source eligibility, readable eligibility, terminal body, budget,
# semantic inference, source locator
ROWS = (
    (
        "ROOT", "root", "critical",
        "No total effective Boolean procedure decides whether every partial-recursive code halts on every natural input.",
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable",
        "The exact frozen arbitrary-code/arbitrary-input proposition.",
        "required", "required", "required", None, 12,
        "Apply the fixed-input reduction to the fixed-input impossibility without changing the code or input domains.",
        "Stage1_Instances/THM-M-0741/Statement.lean",
    ),
    (
        "S-TARGET", "definition", "critical",
        "Freeze Code x Nat, Code.eval domain semantics, and ComputablePred as one uniform effective-decider contract.",
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable",
        "The canonical binders, definitions, and conclusion with no hidden premise.",
        "informational", "not_applicable", "required", None, 16,
        "Unfold only the local Halts name and preserve the exact elaborated expression fingerprint.",
        "Stage1_Instances/THM-M-0741/statement.json",
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Retain every code and natural input, including zero, an immediately terminating code, and a witnessed divergent code.",
        "Stage1Instances.THM_M_0741.{zero_halts,rfind_succ_does_not_halt}",
        "The exhaustive validity and execution-semantics boundary.",
        "informational", "required", "required",
        "local:Stage1_Instances/THM-M-0741/Statement.lean#zero_halts+rfind_succ_does_not_halt",
        18,
        "Use definedness of Code.eval rather than bounded execution, special output values, or malformed-code filtering.",
        "Stage1_Instances/THM-M-0741/Statement.lean",
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit Lean, classical choice, quotient soundness, propositional extensionality, and the no-oracle computation policy.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation and computation boundary.",
        "informational", "not_applicable", "required", None, 36,
        "Compare the machine-derived axiom and executable closure with the selected foundation and TCB profiles.",
        "Stage1_Instances/THM-M-0741/anchor-audit.json",
    ),
    (
        "N-FIXED-ZERO", "reduction", "critical",
        "Reduce arbitrary-pair halting undecidability to undecidability at the fixed input zero.",
        "Stage1Instances.THM_M_0741.ObligationTree.FixedInputReduction",
        "FixedInputZeroUndecidable implies the exact canonical root.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0741/ObligationTree.lean#fixedInputReduction_of_restriction",
        16,
        "Turn restriction of any alleged pair decider into the contradiction required by the fixed-input theorem.",
        "Stage1_Instances/THM-M-0741/ObligationTree.lean",
    ),
    (
        "C-PAIR-ZERO", "construction", "high",
        "Construct the computable section code maps to (code, 0).",
        "Stage1Instances.THM_M_0741.ObligationTree.PairZeroEmbeddingComputable",
        "Computability of the pair-zero embedding.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0741/ObligationTree.lean#pairZeroEmbedding_computable",
        10,
        "Pair Computable.id with Computable.const 0, preserving the original code exactly.",
        "Stage1_Instances/THM-M-0741/ObligationTree.lean",
    ),
    (
        "L-RESTRICT", "core_lemma", "critical",
        "Restrict both components of ComputablePred along the pair-zero embedding.",
        "Stage1Instances.THM_M_0741.ObligationTree.PairToFixedRestriction",
        "A pair decider yields a fixed-input-zero decider.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0741/ObligationTree.lean#pairToFixedRestriction_of_embedding",
        24,
        "Reuse the DecidablePred witness at (code, 0) and compose its computable Boolean characteristic with the embedding.",
        "Stage1_Instances/THM-M-0741/ObligationTree.lean",
    ),
    (
        "X-FIXED-HALTING", "bridge", "critical",
        "The fixed-input-zero halting predicate is not computable.",
        "ComputablePred.halting_problem 0",
        "FixedInputZeroUndecidable at the exact normalized input.",
        "required", "required", "required", MATHLIB_HALTING_BODY, 14,
        "Instantiate the pinned fixed-input theorem at zero; keep its Rice dependency and witnesses explicit below this bridge.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean:241",
    ),
    (
        "X-RICE", "bridge", "critical",
        "A computable semantic predicate on codes cannot distinguish two represented partial functions with different membership.",
        "ComputablePred.rice",
        "The exact RiceBridge transfer interface used by fixed-input halting.",
        "required", "required", "required", MATHLIB_RICE_BODY, 30,
        "Use the pinned fixed-point conditional construction and exhaustive membership split to transfer semantic membership.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean:209",
    ),
    (
        "L-FIXED-POINT", "bridge", "critical",
        "Produce a self-referential code whose evaluation agrees with the conditional partial-recursive construction.",
        "Nat.Partrec.Code.fixed_point2 as used by ComputablePred.rice",
        "The fixed-point code and its evaluation equation.",
        "informational", "required", "required", None, 50,
        "Apply the pinned binary fixed-point theorem to the conditional program built from the semantic decider and two represented functions.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean:213",
    ),
    (
        "C-CONDITIONAL", "construction", "critical",
        "Construct the partial-recursive program that selects between the represented positive and negative functions using the alleged semantic decider.",
        "Nat.Partrec.cond construction inside ComputablePred.rice",
        "A represented conditional partial function suitable for fixed-point formation.",
        "informational", "required", "required", None, 45,
        "Compose the alleged Boolean decider with projections and use Partrec.cond on the two represented branches.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean:214",
    ),
    (
        "B-MEMBERSHIP", "branch", "critical",
        "Split exhaustively on whether the fixed-point evaluation belongs to the semantic class and close both cases by the fixed-point equation.",
        "the by_cases membership split inside ComputablePred.rice",
        "Membership transfer from the represented positive function to the represented negative function.",
        "informational", "required", "required", MATHLIB_RICE_BODY, 35,
        "Analyze both truth values of fixed-point membership; simplification with the fixed-point equation forces the required transfer in either branch.",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean:217",
    ),
    (
        "B-FIXED-WITNESSES", "branch", "high",
        "Exhibit one represented function defined at zero and one represented function undefined at zero.",
        "Stage1Instances.THM_M_0741.ObligationTree.FixedZeroWitnessPackage",
        "Positive and negative witnesses for the semantic class partial maps defined at zero.",
        "required", "required", "required",
        "local:Stage1_Instances/THM-M-0741/ObligationTree.lean#fixedZeroWitnessPackage",
        18,
        "Choose the everywhere-zero partial function and the nowhere-defined partial function, then verify representation and opposite domain membership.",
        "Stage1_Instances/THM-M-0741/ObligationTree.lean",
    ),
    (
        "T-COMPOSITION", "certificate", "critical",
        "Check every available child-to-parent interface without installing the imported Rice or fixed-input proof bodies.",
        "the four composition declarations in Stage1Instances.THM_M_0741.ObligationTree",
        "Exact conditional compositions for restriction, normalization, fixed-input contradiction, and the canonical root.",
        "informational", "not_applicable", "required",
        "local:Stage1_Instances/THM-M-0741/ObligationTree.lean#root_of_reduction_and_fixedInput",
        30,
        "Elaborate abstract-child harnesses, bind their exact parent and child fingerprints, and reject undeclared premises.",
        "Stage1_Instances/THM-M-0741/ObligationTree.lean",
    ),
    (
        "X-SOURCE", "terminal", "high",
        "Pinpoint and independently review the primary halting proof, machine model, correction history, and every material reduction node.",
        "primary-source packet and independent review pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", "required", None, 60,
        "Map primary-source premises and transitions to the exact code semantics, fixed-input reduction, Rice bridge, and witness obligations.",
        "Stage1_Instances/THM-M-0741/source-statement-crosswalk.md",
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Bind wrappers, terminal bodies, imports, revisions, source blobs, licenses, and aliases without duplicate proof credit.",
        "content-addressed terminal and transitive provenance closure",
        "Release-grade body provenance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 50,
        "Trace the local interfaces to the single pinned halting body and its Rice dependency, then hash the full transitive declaration closure.",
        "Stage1_Instances/THM-M-0741/anchor-audit.json",
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit toolchain, compiled artifacts, axioms, unsafe and oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0 and mathlib 8a178386 transitive trust closure",
        "Release trust evidence without proof credit.",
        "informational", "not_applicable", "required", None, 50,
        "Recompute the exact declaration, artifact, executable, axiom, and no-oracle closure in a hermetic verifier.",
        "Stage1_Instances/THM-M-0741/anchor-audit.json",
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide a complete independently reviewed reconstruction of the reduction and Rice fixed-point argument.",
        "node-specific readable reconstruction and review pending",
        "Readable proof coverage without machine proof credit.",
        "not_applicable", "not_applicable", "required", None, 75,
        "Expand every high-risk bridge into premise-to-inference-to-output steps and obtain an independent mathematical reading decision.",
        "Stage1_Instances/THM-M-0741/obligation-tree.md",
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind dependency-legal proof, validation, release, freshness, revocation, and independent-verification acceptance.",
        "Stage1 rev-5.6 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", "required", None, 30,
        "Require accepted predecessor receipts before proof adoption and accepted proof, validation, and release receipts before terminal decisions.",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
    ),
)


REQUIRES = {
    oid("ROOT"): [oid("N-FIXED-ZERO"), oid("X-FIXED-HALTING")],
    oid("N-FIXED-ZERO"): [oid("L-RESTRICT")],
    oid("L-RESTRICT"): [oid("C-PAIR-ZERO")],
    oid("X-FIXED-HALTING"): [oid("X-RICE"), oid("B-FIXED-WITNESSES")],
}

CERTIFICATE_DECLARATIONS = {
    oid("ROOT"): "Stage1Instances.THM_M_0741.ObligationTree.root_of_reduction_and_fixedInput",
    oid("N-FIXED-ZERO"): "Stage1Instances.THM_M_0741.ObligationTree.fixedInputReduction_of_restriction",
    oid("L-RESTRICT"): "Stage1Instances.THM_M_0741.ObligationTree.pairToFixedRestriction_of_embedding",
    oid("X-FIXED-HALTING"): "Stage1Instances.THM_M_0741.ObligationTree.fixedInputZeroUndecidable_of_rice",
}


def edge(
    edge_id: str,
    source: str,
    edge_type: str,
    target: str,
    reciprocal: str | None = None,
) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(edges: list[dict]) -> dict:
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusion_reasons = {
        oid("S-TARGET"): "expository_statement_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("S-BOUNDARY"): "expository_boundary_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("S-FOUNDATION"): "release_foundation_overlay_no_proof_credit_pending_independent_approval",
        oid("L-FIXED-POINT"): "expository_rice_body_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("C-CONDITIONAL"): "expository_rice_body_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("B-MEMBERSHIP"): "expository_rice_body_overlay_no_independent_machine_credit_pending_independent_approval",
        oid("T-COMPOSITION"): "composition_certificate_overlay_no_independent_semantic_credit_pending_independent_approval",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }

    parent_of: dict[str, list[str]] = {}
    for parent, children in REQUIRES.items():
        for child in children:
            parent_of.setdefault(child, []).append(parent)

    for (
        short, kind, risk, claim, formal, output, machine, human_source,
        readable, body, budget, inference, source_locator,
    ) in ROWS:
        identifier = oid(short)
        if identifier in {oid("ROOT"), oid("S-TARGET")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest(
                [identifier, kind, claim, formal, output]
            )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": True,
                "machine_eligibility": machine,
                "human_source_eligibility": human_source,
                "readable_eligibility": readable,
                "risk_class": risk,
                "exclusion_reason": exclusion_reasons.get(identifier),
                "terminal_proof_body_id": body,
            }
        )

        if identifier == oid("X-FIXED-HALTING"):
            provenance = "anchor-audit:M0741-C02-MATHLIB-FIXED-INPUT"
        elif identifier in {
            oid("X-RICE"), oid("L-FIXED-POINT"), oid("C-CONDITIONAL"),
            oid("B-MEMBERSHIP"),
        }:
            provenance = "anchor-audit:M0741-C03-MATHLIB-ADJACENT"
        elif body and body.startswith("local:"):
            provenance = "target-local-conditional-composition"
        else:
            provenance = "none"

        owned_sources: list[str] = []
        if identifier in {oid("S-TARGET"), oid("S-BOUNDARY")}:
            owned_sources = ["Stage1_Instances/THM-M-0741/Statement.lean"]
        elif identifier in {
            oid("N-FIXED-ZERO"), oid("C-PAIR-ZERO"), oid("L-RESTRICT"),
            oid("B-FIXED-WITNESSES"), oid("T-COMPOSITION"),
        }:
            owned_sources = ["Stage1_Instances/THM-M-0741/ObligationTree.lean"]
        elif identifier == oid("X-SOURCE"):
            owned_sources = ["Stage1_Instances/THM-M-0741/source-statement-crosswalk.md"]
        elif identifier == oid("X-READABLE"):
            owned_sources = ["Stage1_Instances/THM-M-0741/obligation-tree.md"]

        premise_ids = REQUIRES.get(identifier, [])
        if not premise_ids:
            premise_ids = [
                "pinned-mathlib-source"
                if identifier in {
                    oid("X-RICE"), oid("L-FIXED-POINT"),
                    oid("C-CONDITIONAL"), oid("B-MEMBERSHIP"),
                }
                else "frozen-formal-context"
            ]
        outgoing_use = (
            "Consumed by " + ", ".join(parent_of[identifier]) + "."
            if identifier in parent_of
            else "Supports a typed refinement, release, documentation, or workflow edge only."
        )
        task_ids = [ITEM]
        if machine == "required":
            task_ids.append("S56-M-0741-PROOF")
        if identifier in {
            oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"),
        }:
            task_ids.extend(["S56-M-0741-VALIDATION", "S56-M-0741-RELEASE"])
        if identifier in {oid("X-SOURCE"), oid("X-READABLE"), oid("X-WORKFLOW")}:
            task_ids.append("S56-M-0741-RELEASE")

        nodes.append(
            {
                "node_id": f"{THEOREM}-{short}",
                "obligation_id": identifier,
                "kind": kind,
                "human_statement": claim,
                "formal_target": formal,
                "output": output,
                "human_debt": "H1",
                "machine_debt": "M3" if machine != "not_applicable" else "M4",
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "primary-source-node-map-pending"
                    if human_source == "required"
                    else "not-applicable-pending-review"
                ),
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory; propext, Classical.choice, and Quot.sound observed; acceptance pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive executable and artifact closure pending",
                "computation_record": "none; no native computation, solver, oracle, timeout, experiment, or unchecked certificate is credited",
                "step_budget": budget,
                "semantic_step_ledger": [
                    {
                        "step_id": f"STEP-{identifier}-01",
                        "premise_ids": premise_ids,
                        "inference": inference,
                        "source_locator": source_locator,
                        "output": output,
                        "outgoing_use": outgoing_use,
                    }
                ],
                "public_readable_target": (
                    f"Stage1_Instances/THM-M-0741/obligation-tree.md#{identifier.lower()}"
                ),
                "validation_spec_id": "VAL-M0741-OBLIGATION-BUNDLE",
                "status_boundary": "Frozen architecture, source-body mapping, or conditional interface only; no M0, H0, R0, accepted root, audit completion, or theorem completion is credited.",
                "task_ids": task_ids,
                "owned_sources": owned_sources,
                "owner": "THM-M-0741 execution lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13",
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": [
                        "Statement.lean", "anchor-audit.json",
                        "obligation-registry.json", "typed-graphs.json",
                        "ObligationTree.lean", "toolchain and dependency pins",
                    ],
                    "revocation_state": "not-accepted",
                },
            }
        )

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility",
        "readable_eligibility", "risk_class", "exclusion_reason",
        "terminal_proof_body_id",
    )
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0741-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T20:41:15+08:00",
        "freeze_basis": "The exact elaborated pair target, bounded immutable anchor inventory, and visible source architecture of the pinned halting and Rice bodies. Eligibility and denominators are fixed independently of candidate success or closure credit.",
        "freeze_timing_boundary": "The workflow places this phase after anchor audit, so the available candidate route was already observed. No blind pre-discovery freeze is claimed; the registry nevertheless includes every statement, normalization, branch, construction, imported theorem, source, trust, readability, and workflow boundary before any closure metric is recorded.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [
                row["obligation_id"] for row in obligations
                if row["machine_eligibility"] == "required"
            ],
            "required_human_source": [
                row["obligation_id"] for row in obligations
                if row["human_source_eligibility"] == "required"
            ],
            "required_readable": [
                row["obligation_id"] for row in obligations
                if row["readable_eligibility"] == "required"
            ],
            "informational_overlays": [
                row["obligation_id"] for row in obligations
                if row["machine_eligibility"] == "informational"
            ],
        },
        "layer_exclusions": {
            "additional_representative_symmetry_or_order_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The route uses the explicit fixed-input-zero reduction and no representative quotient, sign, symmetry, parity, ordering, finite/infinite, or local/global normalization.",
            },
            "additional_root_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "All codes and inputs remain in scope. The only material case split in the visible imported route is the exhaustive fixed-point membership split M0741-B-MEMBERSHIP; the positive and negative fixed-input witnesses are M0741-B-FIXED-WITNESSES.",
            },
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, finite search, numerical approximation, native evaluator, oracle, timeout, experiment, or external certificate participates in the proof route.",
            },
        },
        "proof_body_aliases": {
            "ComputablePred.halting_problem 0": "canonical_terminal_body:ComputablePred.halting_problem",
            "target_owned_fixed_input_interface": "deduplicated_to:ComputablePred.halting_problem",
            "ComputablePred.rice_as_direct_dependency": "single_shared_body:ComputablePred.rice",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility or risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta; version 1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "provisionally_elaborated_interfaces": [
                oid("N-FIXED-ZERO"), oid("C-PAIR-ZERO"), oid("L-RESTRICT"),
                oid("B-FIXED-WITNESSES"), oid("T-COMPOSITION"),
            ],
            "candidate_terminal_obligations": [oid("X-FIXED-HALTING"), oid("X-RICE")],
            "candidate_route": "M0-W-shaped after E1, proof-phase adoption, validation, and master acceptance; current evidence remains below E1",
            "accepted_closed_obligations": [],
            "accepted_root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. Conditional interfaces are not installed proof bodies, the pinned route remains an M3 candidate, and no H0, M0, R0, accepted obligation, audit completion, theorem completion, release, or master acceptance is claimed.",
    }

    proof_edges: list[dict] = []
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof_edges.extend(
                [
                    edge(req, parent, "proof_requires", child, comp),
                    edge(comp, child, "composes", parent, req),
                ]
            )

    source_required = [
        row["obligation_id"] for row in obligations
        if row["human_source_eligibility"] == "required"
        and row["obligation_id"] != oid("X-SOURCE")
    ]
    machine_nodes = [
        row["obligation_id"] for row in obligations
        if row["machine_eligibility"] == "required"
    ]
    readable_nodes = [
        row["obligation_id"] for row in obligations
        if row["readable_eligibility"] == "required"
        and row["obligation_id"] != oid("X-READABLE")
    ]
    workflow_tasks = [
        "S56-M-0741-STATEMENT",
        "S56-M-0741-ANCHOR_AUDIT",
        ITEM,
        "S56-M-0741-PROOF",
        "S56-M-0741-VALIDATION",
        "S56-M-0741-RELEASE",
    ]

    graph_edges = {
        "proof": proof_edges,
        "refinement": [
            edge("REF-ROOT-TARGET", oid("ROOT"), "expository_decomposition", oid("S-TARGET")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
            edge("REF-RICE-FIXED-POINT", oid("X-RICE"), "expository_decomposition", oid("L-FIXED-POINT")),
            edge("REF-RICE-CONDITIONAL", oid("X-RICE"), "expository_decomposition", oid("C-CONDITIONAL")),
            edge("REF-RICE-MEMBERSHIP", oid("X-RICE"), "expository_decomposition", oid("B-MEMBERSHIP")),
        ],
        "provenance": [
            *[
                edge(f"SRC-{index:02d}", source, "source_map", oid("X-SOURCE"))
                for index, source in enumerate(source_required, 1)
            ],
            *[
                edge(f"PROV-{index:02d}", oid("X-PROVENANCE"), "provenance_of", target)
                for index, target in enumerate(machine_nodes, 1)
            ],
        ],
        "evidence": [
            edge(f"EVID-{index:02d}", oid("X-PROVENANCE"), "evidence_for", target)
            for index, target in enumerate(machine_nodes, 1)
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-RELEASE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-HALTING", oid("X-FIXED-HALTING"), "trusts", oid("X-TRUST")),
            edge("TRUST-RICE", oid("X-RICE"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            *[
                edge(f"DOC-{index:02d}", oid("X-READABLE"), "documents", target)
                for index, target in enumerate(readable_nodes, 1)
            ],
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-ANCHOR-STATEMENT", "S56-M-0741-ANCHOR_AUDIT", "workflow_depends_on", "S56-M-0741-STATEMENT"),
            edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0741-ANCHOR_AUDIT"),
            edge("FLOW-PROOF-TREE", "S56-M-0741-PROOF", "workflow_depends_on", ITEM),
            edge("FLOW-VALIDATION-PROOF", "S56-M-0741-VALIDATION", "workflow_depends_on", "S56-M-0741-PROOF"),
            edge("FLOW-RELEASE-VALIDATION", "S56-M-0741-RELEASE", "workflow_depends_on", "S56-M-0741-VALIDATION"),
        ],
    }

    certificates = []
    for parent, declaration in CERTIFICATE_DECLARATIONS.items():
        children = REQUIRES[parent]
        certificates.append(
            {
                "certificate_id": "COMP-" + parent,
                "parent_obligation_id": parent,
                "parent_statement_fingerprint": fingerprints[parent],
                "required_child_ids": children,
                "required_child_statement_fingerprints": {
                    child: fingerprints[child] for child in children
                },
                "checked_declaration": declaration,
                "certificate_kind": "lean_abstract_child_harness",
                "introduces_undeclared_premises": False,
                "status": "provisionally_elaborated_not_accepted",
            }
        )

    graphs = {name: graph(graph_edges[name]) for name in GRAPH_NAMES}
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "obligation IDs except workflow, whose endpoints are workflow_task_nodes",
        "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent; support edges never carry machine proof credit",
        "workflow_task_nodes": workflow_tasks,
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": certificates,
        "unverified_decomposition_plans": [],
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": [
                oid("C-PAIR-ZERO"), oid("X-RICE"), oid("B-FIXED-WITNESSES"),
            ],
            "remaining_root_cut_set": [
                oid("X-FIXED-HALTING"), oid("X-SOURCE"),
                oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"),
                oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "candidate_evidence": "The exact fixed-input route is kernel-shaped and locally checked below E1; proof adoption, transitive trust/provenance, and master acceptance remain open.",
            "reason": "Conditional compositions exist, but the imported Rice and fixed-input theorem bodies are not adopted by this phase and every release overlay remains unaccepted.",
        },
    }

    covered_declarations = [
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable",
        "ComputablePred.rice",
        "ComputablePred.halting_problem",
        "Stage1Instances.THM_M_0741.ObligationTree.pairZeroEmbedding_computable",
        "Stage1Instances.THM_M_0741.ObligationTree.pairToFixedRestriction_of_embedding",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedInputReduction_of_restriction",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedZeroWitnessPackage",
        "Stage1Instances.THM_M_0741.ObligationTree.fixedInputZeroUndecidable_of_rice",
        "Stage1Instances.THM_M_0741.ObligationTree.root_of_reduction_and_fixedInput",
    ]
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": "VAL-M0741-OBLIGATION-BUNDLE",
                "cwd": ".",
                "argv": [
                    "python3", "-B",
                    "Stage1_Instances/THM-M-0741/check_obligation_tree.py",
                ],
                "env_allowlist": {},
                "timeout_seconds": 240,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0741 obligation tree",
                    }
                ],
                "covered_obligation_ids": ids,
                "covered_declarations": covered_declarations,
            }
        ],
    }
    return registry, bundle, recipes


def main() -> None:
    registry, bundle, recipes = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
    edge_count = sum(
        len(graph_value["edges"])
        for graph_value in bundle["graphs"].values()
    )
    print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
