#!/usr/bin/env python3
"""Build the frozen THM-M-0912 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0912-OBLIGATION_TREE"
THEOREM = "THM-M-0912"
PREFIX = "M0912-"
ROOT_EXPRESSION = "b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776"
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


# short id, kind, risk, human statement, formal target, output,
# machine eligibility, human-source eligibility, terminal body, step budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "For natural m and n with n <= m and 1 <= n, Pascal's predecessor recurrence holds in the DLMF summand order.",
        "Stage1Instances.THM_M_0912.PascalIdentityTarget",
        "The exact frozen constrained Pascal-identity proposition.",
        "required", "required", None, 8,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Freeze natural row and column binders, premises n <= m and 1 <= n, and the source's predecessor-form conclusion.",
        "Stage1Instances.THM_M_0912.PascalIdentityTarget",
        "The exact binder, domain, hypothesis, and conclusion interface.",
        "required", "not_applicable", None, 10,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Include positive diagonals and exclude column zero and columns beyond the row.",
        "pascalIdentityTarget_includes_diagonal; column_zero_is_excluded; out_of_range_is_excluded",
        "The complete source-domain boundary policy.",
        "required", "required", None, 12,
    ),
    (
        "S-TRANSPORTS", "transport", "high",
        "Relate the canonical target to the DLMF conjunction, reversed-summand, and restricted successor encodings without broadening the root.",
        "pascalIdentityTarget_iff_dlmfConjunctionTarget; pascalIdentityTarget_iff_mathlibSummandOrderTarget; pascalIdentityTarget_iff_restrictedSuccessorTarget",
        "Three checked bidirectional statement transports.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0912.pascalIdentityTarget_iff_mathlibSummandOrderTarget", 18,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Fix Lean natural-number recursion, equality, propositional extensionality policy, and the no-oracle computation boundary.",
        "Lean 4.29.0 foundation and transitive axiom report",
        "An accepted foundation, computation, and TCB boundary.",
        "required", "not_applicable", None, 24,
    ),
    (
        "N-POSITIVE-ROW", "normalization", "high",
        "Derive 0 < m from 1 <= n and n <= m.",
        "Stage1Instances.THM_M_0912.ObligationTree.PositiveRowBridge",
        "The positive-row premise required by the pinned predecessor recurrence.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0912.ObligationTree.positiveRowBridge_checked", 4,
    ),
    (
        "N-SUMMAND-ORDER", "normalization", "normal",
        "Commute the two natural summands returned by mathlib into the DLMF display order.",
        "Stage1Instances.THM_M_0912.ObligationTree.SummandOrderBridge",
        "A checked equality transport from b + c to c + b.",
        "required", "not_applicable",
        "repo:Stage1Instances.THM_M_0912.ObligationTree.summandOrderBridge_checked", 3,
    ),
    (
        "L-CHOOSE-SUCC-RIGHT", "bridge", "high",
        "Expand a positive-row coefficient at a successor column into the two predecessor-row coefficients.",
        "Nat.choose_succ_right",
        "The imported recurrence used inside Nat.choose_eq_choose_pred_add.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Nat.choose_succ_right", 8,
    ),
    (
        "L-POSITIVE-COLUMN-REINDEX", "core_lemma", "normal",
        "Represent a positive column as k + 1 and cancel the successor predecessor expression.",
        "Nat.exists_eq_add_of_le'; Nat.add_one_sub_one",
        "The positive-column reindexing used by the terminal theorem body.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Nat.exists_eq_add_of_le'+Nat.add_one_sub_one", 8,
    ),
    (
        "T-PREDECESSOR-COMPOSE", "terminal", "critical",
        "Compose the positive-column reindexing and choose_succ_right into the exact predecessor recurrence.",
        "Nat.choose_eq_choose_pred_add",
        "The exact mathlib-order recurrence anchor.",
        "required", "required",
        f"mathlib:{MATHLIB_REVISION}:Nat.choose_eq_choose_pred_add", 12,
    ),
    (
        "T-ROOT-COMPOSE", "terminal", "critical",
        "Consume row positivity, the predecessor recurrence, and summand-order transport to yield the frozen root.",
        "Stage1Instances.THM_M_0912.ObligationTree.root_of_bridges_and_predecessorAnchor",
        "The architecture-local root, definitionally identical to the canonical target.",
        "required", "required",
        "repo:Stage1Instances.THM_M_0912.ObligationTree.root_of_bridges_and_predecessorAnchor", 8,
    ),
    (
        "X-SOURCE", "source_boundary", "high",
        "Pinpoint and independently review the exact primary human proof, assumptions, definitions, historical attribution, and errata.",
        "primary-source packet and independent review pending",
        "Human-source coverage without machine proof credit.",
        "not_applicable", "required", None, 30,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Audit wrapper/body/conclusion identities, immutable source blobs, origin commits, imports, aliases, and licenses.",
        "Nat.choose_eq_choose_pred_add at pinned mathlib plus transitive declarations",
        "Body-level provenance without duplicate semantic credit.",
        "informational", "not_applicable", None, 30,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit Lean, mathlib, declaration axioms, compiled objects, unsafe and oracle boundaries, replay, and supply-chain trust transitively.",
        "Lean 4.29.0; mathlib 8a178386; transitive closure pending",
        "Release-grade trust inventory without mathematical proof credit.",
        "informational", "not_applicable", None, 35,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a complete readable counting or recursive-definition proof mapped to every mathematical node.",
        "node-specific readable reconstruction pending",
        "Readable coverage and reviewer decision without machine proof credit.",
        "not_applicable", "required", None, 35,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
        "Stage1 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 20,
    ),
)

CHECKED_INTERFACES = {
    oid("S-INTERFACE"),
    oid("S-BOUNDARY"),
    oid("S-TRANSPORTS"),
    oid("N-POSITIVE-ROW"),
    oid("N-SUMMAND-ORDER"),
    oid("T-ROOT-COMPOSE"),
}
SOURCE_NA = {
    oid("S-INTERFACE"),
    oid("S-TRANSPORTS"),
    oid("S-FOUNDATION"),
    oid("N-SUMMAND-ORDER"),
    oid("X-PROVENANCE"),
    oid("X-TRUST"),
    oid("X-WORKFLOW"),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []
    exclusion_reasons = {
        oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-TRANSPORTS"): "formal_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
        oid("N-SUMMAND-ORDER"): "formal_commutativity_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }
    anchor_nodes = {oid("T-PREDECESSOR-COMPOSE")}

    for short, kind, risk, claim, target, result, machine, human, body, budget in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")}
            else "planned:v1:sha256:" + digest([identifier, kind, claim, target, result])
        )
        obligations.append(
            {
                "obligation_id": identifier,
                "statement_fingerprint": fingerprint,
                "kind": kind,
                "root_relevant": True,
                "machine_eligibility": machine,
                "human_source_eligibility": human,
                "readable_eligibility": "required",
                "risk_class": risk,
                "exclusion_reason": exclusion_reasons.get(identifier),
                "terminal_proof_body_id": body,
            }
        )

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier in anchor_nodes or identifier in {
            oid("L-CHOOSE-SUCC-RIGHT"), oid("L-POSITIVE-COLUMN-REINDEX")
        }:
            machine_debt = "M3"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier in anchor_nodes:
            provenance = "anchor-audit:M0912-C01-MATHLIB-PREDECESSOR"
        elif identifier == oid("L-CHOOSE-SUCC-RIGHT"):
            provenance = "pinned-mathlib:Nat.choose_succ_right"
        elif identifier == oid("L-POSITIVE-COLUMN-REINDEX"):
            provenance = "pinned-mathlib:Nat.exists_eq_add_of_le'+Nat.add_one_sub_one"
        elif identifier in {oid("N-POSITIVE-ROW"), oid("N-SUMMAND-ORDER"), oid("T-ROOT-COMPOSE")}:
            provenance = "local-conditional-composition"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {oid("N-POSITIVE-ROW"), oid("N-SUMMAND-ORDER"), oid("T-ROOT-COMPOSE")}:
            owned_sources = ["Stage1_Instances/THM-M-0912/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-TRANSPORTS")}:
            owned_sources = ["Stage1_Instances/THM-M-0912/Statement.lean"]

        nodes.append(
            {
                "node_id": f"{THEOREM}-{short}",
                "obligation_id": identifier,
                "kind": kind,
                "human_statement": claim,
                "formal_target": target,
                "output": result,
                "human_debt": "H1",
                "machine_debt": machine_debt,
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": (
                    "not-applicable-pending-review"
                    if identifier in SOURCE_NA else "primary-source-node-map-pending"
                ),
                "provenance_id": provenance,
                "foundation_profile": "lean4-dependent-type-theory-nat-recursion; accepted axiom policy and transitive review pending",
                "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
                "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
                "step_budget": budget,
                "semantic_step_ledger": {
                    "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                    "inference": target,
                    "output": result,
                    "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0912/obligation-tree.md#{identifier.lower()}",
                "validation_spec_id": f"VAL-{identifier}",
                "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
                "task_ids": [ITEM, "S56-M-0912-PROOF"],
                "owned_sources": owned_sources,
                "owner": "THM-M-0912 proof lane",
                "reviewer": "independent Stage1 integration lane",
                "validity": {
                    "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": [
                        "Statement.lean",
                        "anchor-audit.json",
                        "obligation-registry.json",
                        "typed-graphs.json",
                        "toolchain and dependency pins",
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
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0912-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T23:30:00+08:00",
        "freeze_basis": "The exact statement and semantic architecture of the selected predecessor route. Eligibility and denominators are independent of proof acceptance; anchor status is recorded only after the freeze.",
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
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The source domain makes column positivity and row positivity explicit; the recurrence proof contains no parity, induction, local/global, or other branch beyond the separately modeled boundary policy.",
            },
            "construction": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The route constructs no new mathematical object; Nat.choose is a pinned recursive definition represented at the external boundary.",
            },
            "computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "No reflection, solver, numerical table, native code, oracle, experiment, or certificate proves the universal target.",
            },
        },
        "proof_body_aliases": {
            "Nat.choose_succ_succ": "same Nat.choose recursive definition family; adjacent interface only",
            "Nat.choose_succ_succ'": "same Nat.choose recursive definition family; alternate checked adapter only",
            "Nat.choose_succ_left": "same predecessor recurrence family; no duplicate semantic credit",
            "M0912-C02-MATHLIB-SUCCESSOR": "deduplicated_to:M0912-C01-MATHLIB-PREDECESSOR",
        },
        "delta_policy": "Any target change, correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligations": sorted(anchor_nodes),
            "audited_candidate_classification": "M0-W route candidate pending proof-phase adoption and master acceptance",
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
        oid("T-ROOT-COMPOSE"): [
            oid("N-POSITIVE-ROW"), oid("T-PREDECESSOR-COMPOSE"), oid("N-SUMMAND-ORDER")
        ],
        oid("T-PREDECESSOR-COMPOSE"): [
            oid("L-CHOOSE-SUCC-RIGHT"), oid("L-POSITIVE-COLUMN-REINDEX")
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
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "expository_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-TRANSPORTS", oid("ROOT"), "transports", oid("S-TRANSPORTS")),
        ],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-PREDECESSOR", oid("X-SOURCE"), "source_map", oid("T-PREDECESSOR-COMPOSE")),
            edge("PROV-PREDECESSOR", oid("X-PROVENANCE"), "provenance_of", oid("T-PREDECESSOR-COMPOSE")),
            edge("PROV-SUCC-RIGHT", oid("X-PROVENANCE"), "provenance_of", oid("L-CHOOSE-SUCC-RIGHT")),
        ],
        "evidence": [
            edge("EVID-ANCHOR", oid("X-PROVENANCE"), "evidence_for", oid("T-PREDECESSOR-COMPOSE")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-ANCHOR-CLOSURE", oid("T-PREDECESSOR-COMPOSE"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-PREDECESSOR", oid("X-READABLE"), "documents", oid("T-PREDECESSOR-COMPOSE")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("T-PREDECESSOR-COMPOSE")),
            edge("FLOW-PROVENANCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
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
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_only_obligations": sorted(anchor_nodes),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("T-PREDECESSOR-COMPOSE"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0912.ObligationTree.positiveRowBridge_checked",
                "Stage1Instances.THM_M_0912.ObligationTree.summandOrderBridge_checked",
                "Stage1Instances.THM_M_0912.ObligationTree.predecessorRecurrence_of_chooseSuccRight_and_reindex",
                "Stage1Instances.THM_M_0912.ObligationTree.root_of_bridges_and_predecessorAnchor",
            ],
            "reason": "Every root composition is conditional; the exact pinned predecessor anchor remains uninstalled and unaccepted until proof-phase and master validation.",
        },
    }

    declaration_map = {
        oid("ROOT"): ["Stage1Instances.THM_M_0912.PascalIdentityTarget"],
        oid("N-POSITIVE-ROW"): ["Stage1Instances.THM_M_0912.ObligationTree.positiveRowBridge_checked"],
        oid("N-SUMMAND-ORDER"): ["Stage1Instances.THM_M_0912.ObligationTree.summandOrderBridge_checked"],
        oid("L-CHOOSE-SUCC-RIGHT"): ["Nat.choose_succ_right"],
        oid("T-PREDECESSOR-COMPOSE"): [
            "Nat.choose_eq_choose_pred_add",
            "Stage1Instances.THM_M_0912.ObligationTree.predecessorRecurrence_of_chooseSuccRight_and_reindex",
        ],
        oid("T-ROOT-COMPOSE"): ["Stage1Instances.THM_M_0912.ObligationTree.root_of_bridges_and_predecessorAnchor"],
    }
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [],
    }
    for identifier in ids:
        recipes["recipes"].append(
            {
                "recipe_id": f"VAL-{identifier}",
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0912/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [
                    {
                        "path_or_stream": "stdout",
                        "semantic_hash_policy": "contains PASS THM-M-0912 obligation tree",
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
