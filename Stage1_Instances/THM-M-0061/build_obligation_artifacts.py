#!/usr/bin/env python3
"""Build the frozen THM-M-0061 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0061-OBLIGATION_TREE"
THEOREM = "THM-M-0061"
PREFIX = "M0061-"
ROOT_EXPRESSION = "adff72e9052ea17e3b6e4349c23028f35f4b8e3c610ea5f9f3b4fc02fe136836"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# Eligibility and risk in this architecture table are fixed independently of closure status.
# short id, kind, risk, human statement, formal target, output, machine eligibility,
# human-source eligibility, terminal proof-body identity, step budget
ROWS = (
    ("ROOT", "root", "critical",
     "For every finite group G and subgroup H, Nat.card H divides Nat.card G.",
     "Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget",
     "The exact frozen finite-group proposition.", "required", "required", None, 8),
    ("S-INTERFACE", "definition", "high",
     "Freeze the universe, Group then Finite typeclass binders, arbitrary subgroup, Nat.card, and natural divisibility conclusion.",
     "Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget",
     "The exact domain, binder order, and conclusion without a stronger or narrower substitution.",
     "required", "not_applicable", None, 14),
    ("S-BOUNDARY", "branch", "high",
     "Retain the trivial group and bottom and top subgroups; add no normality, properness, nontriviality, commutativity, or cyclicity premise.",
     "Statement.lean boundary witnesses and mutation suite",
     "The complete degenerate-case policy.", "required", "not_applicable", None, 18),
    ("S-FINTYPE-TRANSPORT", "transport", "high",
     "Relate the Finite/Nat.card root bidirectionally to the checked Fintype/Fintype.card encoding without duplicate proof credit.",
     "Stage1Instances.THM_M_0061.lagrangeDivisibilityTarget_iff_fintypeCardTarget",
     "A checked iff transport preserving group, subgroup, universe, and divisibility.",
     "required", "not_applicable",
     "repo:Stage1Instances.THM_M_0061.lagrangeDivisibilityTarget_iff_fintypeCardTarget", 18),
    ("S-FOUNDATION", "certificate", "critical",
     "Fix the Lean kernel, classical choice, quotient soundness, extensionality, computation, and no-oracle policy for the route.",
     "Lean 4.29.0 foundation and transitive axiom report",
     "An accepted foundation and computation boundary.", "informational", "not_applicable", None, 36),
    ("T-FINITE-SCOPE", "terminal", "high",
     "Specialize arbitrary-group Nat.card divisibility to the exact finite-group root while retaining the Finite binder.",
     "Stage1Instances.THM_M_0061.ObligationTree.finiteScope_of_arbitraryGroup",
     "The exact canonical finite-group proposition.", "required", "required",
     "repo:Stage1Instances.THM_M_0061.ObligationTree.finiteScope_of_arbitraryGroup", 8),
    ("A-LAGRANGE", "bridge", "critical",
     "For every group G and subgroup H, Nat.card H divides Nat.card G.",
     "Subgroup.card_subgroup_dvd_card",
     "The stronger arbitrary-group divisibility package consumed by the finite-scope adapter.",
     "required", "required", f"mathlib:{MATHLIB_REVISION}:Subgroup.card_subgroup_dvd_card", 12),
    ("L-CARD-PRODUCT", "core_lemma", "critical",
     "The cardinality of G equals the cardinality of G quotient H times the cardinality of H.",
     "Subgroup.card_eq_card_quotient_mul_card_subgroup",
     "Nat.card G = Nat.card (G quotient H) * Nat.card H.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Subgroup.card_eq_card_quotient_mul_card_subgroup", 14),
    ("L-NATCARD-PROD", "core_lemma", "normal",
     "Nat.card is multiplicative on product types.", "Nat.card_prod",
     "Nat.card (alpha times beta) = Nat.card alpha * Nat.card beta.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Nat.card_prod", 16),
    ("L-NATCARD-CONGR", "core_lemma", "normal",
     "Equivalent types have equal Nat.card.", "Nat.card_congr",
     "An equivalence transports Nat.card equality.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Nat.card_congr", 12),
    ("C-COSET-PRODUCT-EQUIV", "construction", "critical",
     "Construct a non-canonical equivalence G equivalent to (G quotient H) times H.",
     "Subgroup.groupEquivQuotientProdSubgroup",
     "The equivalence consumed by cardinal congruence.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Subgroup.groupEquivQuotientProdSubgroup", 20),
    ("C-FIBER-DECOMPOSITION", "construction", "high",
     "Decompose G into the sigma type of fibers of the quotient map.",
     "(Equiv.sigmaFiberEquiv QuotientGroup.mk).symm",
     "G equivalent to the sigma family of quotient-map fibers.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Equiv.sigmaFiberEquiv", 22),
    ("T-FIBER-TO-COSET", "transport", "high",
     "Identify each quotient-map fiber with the left coset represented by Quotient.out, using Quotient.out_eq' to justify the representative.",
     "QuotientGroup.eq_class_eq_leftCoset plus Quotient.out_eq' and Equiv.sigmaCongrRight",
     "A fiberwise equivalence to the sigma family of left cosets.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Subgroup.groupEquivQuotientProdSubgroup#fiber-to-coset-block", 26),
    ("C-LEFT-COSET-EQUIV", "construction", "high",
     "Translate each left coset by its representative to obtain an equivalence with H.",
     "Subgroup.leftCosetEquivSubgroup",
     "Every left coset is equivalent to the subgroup.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Subgroup.leftCosetEquivSubgroup", 20),
    ("T-SIGMA-PRODUCT", "transport", "normal",
     "Collapse the constant sigma family over G quotient H to the product (G quotient H) times H.",
     "Equiv.sigmaEquivProd",
     "The final sigma-to-product equivalence.", "required", "required",
     f"mathlib:{MATHLIB_REVISION}:Equiv.sigmaEquivProd", 12),
    ("X-SOURCE", "source_boundary", "high",
     "Pinpoint and independently review a primary proof, definitions, assumptions, historical wording, and errata for every mathematical node.",
     "primary-source packet and independent review pending",
     "Human-source coverage without machine proof credit.", "not_applicable", "required", None, 45),
    ("X-PROVENANCE", "certificate", "critical",
     "Audit the exact wrapper and terminal bodies, aliases, source blobs, imports, revisions, and licenses.",
     "pinned mathlib Card.lean and Basic.lean transitive declarations",
     "Body-level provenance without duplicate proof credit.", "informational", "not_applicable", None, 50),
    ("X-TRUST", "certificate", "critical",
     "Audit Lean, mathlib, axioms, compiled artifacts, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
     "Lean 4.29.0; mathlib 8a178386; transitive closure pending",
     "Release-grade trust inventory without mathematical proof credit.", "informational", "not_applicable", None, 50),
    ("X-READABLE", "terminal", "high",
     "Provide and independently review a complete readable reconstruction of the coset-partition proof.",
     "node-specific readable reconstruction pending",
     "Readable coverage and reviewer decision without machine proof credit.", "not_applicable", "required", None, 60),
    ("X-WORKFLOW", "certificate", "high",
     "Bind proof, validation, release, freshness, revocation, and independent-verification task acceptance.",
     "Stage1 workflow receipts pending",
     "Workflow acceptance without mathematical proof credit.", "informational", "not_applicable", None, 30),
)


CHECKED_INTERFACES: set[str] = set()
UPSTREAM_CANDIDATES = {
    oid("A-LAGRANGE"), oid("L-CARD-PRODUCT"), oid("L-NATCARD-PROD"),
    oid("L-NATCARD-CONGR"), oid("C-COSET-PRODUCT-EQUIV"),
    oid("C-FIBER-DECOMPOSITION"), oid("T-FIBER-TO-COSET"),
    oid("C-LEFT-COSET-EQUIV"), oid("T-SIGMA-PRODUCT"),
}
SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-FINTYPE-TRANSPORT"),
    oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW"),
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    exclusions = {
        oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-BOUNDARY"): "formal_boundary_fixture_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FINTYPE-TRANSPORT"): "encoding_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "release_trust_overlay_no_proof_or_human_source_credit_pending_integration_review",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "release_provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "release_trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }
    obligations = []
    nodes = []
    for short, kind, risk, claim, target, output, machine, human_source, body, budget in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")} else
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")},
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })
        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif machine == "required":
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("A-LAGRANGE"):
            provenance = "anchor-audit:M0061-C01-MATHLIB-DIRECT"
        elif identifier in UPSTREAM_CANDIDATES:
            provenance = "pinned-visible-terminal-chain"
        elif identifier == oid("T-FINITE-SCOPE"):
            provenance = "local-conditional-composition"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {oid("T-FINITE-SCOPE"), oid("A-LAGRANGE"), oid("L-CARD-PRODUCT"), oid("C-COSET-PRODUCT-EQUIV")}:
            owned_sources = ["Stage1_Instances/THM-M-0061/ObligationTree.lean"]
        elif identifier == oid("S-FINTYPE-TRANSPORT"):
            owned_sources = ["Stage1_Instances/THM-M-0061/Statement.lean"]
        nodes.append({
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
            "source_crosswalk_id": "not-applicable-pending-review" if identifier in SOURCE_NA else "primary-source-node-map-pending",
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                "inference": target,
                "source_anchors": [target],
                "output": output,
                "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0061/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture, audited candidate, or conditional interface only; no accepted root proof or theorem completion.",
            "task_ids": [ITEM, "S56-M-0061-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0061 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "typed-graphs.json", "toolchain and dependency pins"],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0061-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "The exact frozen statement and visible semantic architecture of the pinned Lagrange body. Eligibility and denominators are fixed independently of candidate closure credit.",
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
            "normalization": {"status": "not_applicable_pending_independent_approval", "reason": "No canonical representative, symmetry, sign/order, local/global, or primitive normalization occurs; finite scope is an explicit transport."},
            "case_split": {"status": "not_applicable_pending_independent_approval", "reason": "The visible proof uses no mathematical branch split; trivial, bottom, and top boundaries remain included in S-BOUNDARY."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No reflection, solver, enumeration, native code, oracle, experiment, or finite certificate participates in the route."},
        },
        "proof_body_aliases": {
            "AddSubgroup.card_addSubgroup_dvd_card": "domain-changing generated duplicate; no multiplicative-root credit",
            "Subgroup.card_eq_card_quotient_mul_card_subgroup": "support body on the same unique route; not a second root proof",
            "Fintype.card_subgroup_dvd_card_encoding": "checked transport to the same canonical root; no duplicate body credit",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility/risk change, or terminal-body identity change requires registry version 2 and an append-only old/new semantic-ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("A-LAGRANGE"),
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
        oid("ROOT"): [oid("T-FINITE-SCOPE")],
        oid("T-FINITE-SCOPE"): [oid("A-LAGRANGE")],
        oid("A-LAGRANGE"): [oid("L-CARD-PRODUCT")],
        oid("L-CARD-PRODUCT"): [oid("L-NATCARD-PROD"), oid("L-NATCARD-CONGR"), oid("C-COSET-PRODUCT-EQUIV")],
        oid("C-COSET-PRODUCT-EQUIV"): [oid("C-FIBER-DECOMPOSITION"), oid("T-FIBER-TO-COSET"), oid("C-LEFT-COSET-EQUIV"), oid("T-SIGMA-PRODUCT")],
    }
    proof = []
    for parent, children in requires.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])
    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "equivalent_to", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-FINTYPE", oid("ROOT"), "transports", oid("S-FINTYPE-TRANSPORT")),
        ],
        "provenance": [
            *[
                edge(f"PROV-{target}", oid("X-PROVENANCE"), "provenance_of", target)
                for target in ids
                if target not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
            ],
            *[
                edge(f"SRC-{target}", oid("X-SOURCE"), "source_map", target)
                for target in ids
                if target != oid("X-SOURCE")
                and next(row for row in obligations if row["obligation_id"] == target)["human_source_eligibility"] == "required"
            ],
        ],
        "evidence": [
            edge("EVID-PROVENANCE-ANCHOR", oid("X-PROVENANCE"), "evidence_for", oid("A-LAGRANGE")),
            edge("EVID-WORKFLOW-ROOT", oid("X-WORKFLOW"), "evidence_for", oid("ROOT")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-ANCHOR-CLOSURE", oid("A-LAGRANGE"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            *[
                edge(f"DOC-{target}", oid("X-READABLE"), "documents", target)
                for target in ids if target != oid("X-READABLE")
            ],
        ],
        "workflow": [
            edge("FLOW-ROOT-PROOF", oid("X-WORKFLOW"), "workflow_depends_on", oid("A-LAGRANGE")),
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
        "registry_id": "THM-M-0061-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_only_obligations": sorted(UPSTREAM_CANDIDATES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("A-LAGRANGE"), oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "composition_certificates": [
                "Stage1Instances.THM_M_0061.ObligationTree.cosetProduct_of_fiber_engines",
                "Stage1Instances.THM_M_0061.ObligationTree.cardProduct_of_engines",
                "Stage1Instances.THM_M_0061.ObligationTree.divisibility_of_cardProduct",
                "Stage1Instances.THM_M_0061.ObligationTree.finiteScope_of_arbitraryGroup",
                "Stage1Instances.THM_M_0061.ObligationTree.root_of_finiteScope",
            ],
            "reason": "All composition checks are conditional; the pinned candidate remains uninstalled and unaccepted until proof-phase and master validation.",
        },
    }
    declaration_map = {
        oid("A-LAGRANGE"): ["Subgroup.card_subgroup_dvd_card"],
        oid("L-CARD-PRODUCT"): ["Subgroup.card_eq_card_quotient_mul_card_subgroup"],
        oid("L-NATCARD-PROD"): ["Nat.card_prod"],
        oid("L-NATCARD-CONGR"): ["Nat.card_congr"],
        oid("C-COSET-PRODUCT-EQUIV"): ["Subgroup.groupEquivQuotientProdSubgroup"],
        oid("C-FIBER-DECOMPOSITION"): ["Equiv.sigmaFiberEquiv"],
        oid("T-FIBER-TO-COSET"): ["QuotientGroup.eq_class_eq_leftCoset", "Quotient.out_eq'", "Equiv.sigmaCongrRight"],
        oid("C-LEFT-COSET-EQUIV"): ["Subgroup.leftCosetEquivSubgroup"],
        oid("T-SIGMA-PRODUCT"): ["Equiv.sigmaEquivProd"],
        oid("A-LAGRANGE"): ["Subgroup.card_subgroup_dvd_card", "Stage1Instances.THM_M_0061.ObligationTree.divisibility_of_cardProduct"],
        oid("T-FINITE-SCOPE"): ["Stage1Instances.THM_M_0061.ObligationTree.finiteScope_of_arbitraryGroup"],
    }
    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
    for identifier in ids:
        recipes["recipes"].append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0061/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0061 obligation tree"}],
            "covered_obligation_ids": (
                [identifier]
                if identifier in CHECKED_INTERFACES else []
            ),
            "covered_declarations": declaration_map.get(identifier, []),
            "coverage_boundary": (
                "exact checked interface coverage"
                if identifier in CHECKED_INTERFACES else
                "structural architecture and candidate-presence check only; no M0 or proof-closure credit"
            ),
        })
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {values[0]['denominator_sha256']}")


if __name__ == "__main__":
    main()
