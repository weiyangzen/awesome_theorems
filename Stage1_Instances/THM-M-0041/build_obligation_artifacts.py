#!/usr/bin/env python3
"""Build the frozen THM-M-0041 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0041-OBLIGATION_TREE"
THEOREM = "THM-M-0041"
PREFIX = "M0041-"
ROOT_EXPRESSION = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_BODY = f"mathlib:{MATHLIB_REVISION}:Matrix.aeval_self_charpoly"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
)
REGISTRY_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def oid(short: str) -> str:
    return PREFIX + short


# short ID, kind, risk, human statement, formal target, output, M eligibility,
# H-source eligibility, terminal body identity, leaf step budget
ROWS = (
    (
        "ROOT", "root", "critical",
        "Every finite square matrix over a commutative ring is annihilated by the determinant-defined characteristic polynomial, including empty index types and zero rings.",
        "Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
        "The exact frozen expanded-determinant Cayley-Hamilton proposition.",
        "required", "required", None, 12,
    ),
    (
        "S-INTERFACE", "definition", "high",
        "Freeze the universes, CommRing coefficient domain, finite decidable square index type, universal matrix binder, Polynomial.aeval, and zero-matrix conclusion.",
        "Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
        "The exact ordered binders and matrix-polynomial evaluation interface.",
        "required", "not_applicable", None, 18,
    ),
    (
        "S-CHARPOLY", "definition", "high",
        "Define the characteristic polynomial as det (X I - A.map C), with coefficients evaluated as scalar matrices.",
        "Stage1Instances.THM_M_0041.characteristicPolynomial",
        "The determinant-defined polynomial used by the canonical target.",
        "required", "required", None, 20,
    ),
    (
        "S-BOUNDARY", "branch", "high",
        "Retain empty finite index types and the zero ring, and introduce no Nonempty, Nontrivial, field, invertibility, or diagonalizability premise.",
        "Stage1Instances.THM_M_0041.CayleyHamiltonTarget; BoundaryProbe.lean",
        "The complete boundary policy for the universal theorem.",
        "required", "required", None, 16,
    ),
    (
        "S-FOUNDATION", "certificate", "critical",
        "Audit the Lean kernel, classical choice, quotient, propositional extensionality, imports, compiled artifacts, and the no-oracle computation boundary.",
        "Lean 4.29.0 foundation and transitive trust report",
        "An accepted foundation, TCB, and computation boundary.",
        "required", "not_applicable", None, 35,
    ),
    (
        "T-CHARPOLY", "transport", "critical",
        "Identify the expanded determinant characteristicPolynomial A definitionally with Matrix.charpoly A in the exact context.",
        "Stage1Instances.THM_M_0041.ObligationTree.CharacteristicPolynomialTransport",
        "For every A, characteristicPolynomial A = Matrix.charpoly A.",
        "required", "required", "repo:characteristicPolynomialTransport", 12,
    ),
    (
        "A-MATHLIB-ANCHOR", "bridge", "critical",
        "Every finite square matrix over a commutative ring is annihilated by Matrix.charpoly.",
        "Stage1Instances.THM_M_0041.ObligationTree.MatrixCayleyHamiltonEngine",
        "For every A, Polynomial.aeval A A.charpoly = 0.",
        "required", "required", MATHLIB_BODY, 18,
    ),
    (
        "C-ADJUGATE", "construction", "critical",
        "Construct the adjugate of the characteristic matrix and use adjugate multiplication to express charpoly A times the identity as adjugate(charmatrix A) times charmatrix A.",
        "Stage1Instances.THM_M_0041.ObligationTree.AdjugateIdentityEngine",
        "Stage1Instances.THM_M_0041.ObligationTree.AdjugateIdentityOutput A for every A.",
        "informational", "required", MATHLIB_BODY, 30,
    ),
    (
        "N-MATPOLY", "normalization", "critical",
        "Transport the matrix-of-polynomials identity through matPolyEquiv and normalize charmatrix A to X - C A.",
        "Stage1Instances.THM_M_0041.ObligationTree.MatrixPolynomialTransportEngine",
        "The corresponding identity in Polynomial (Matrix n n R).",
        "informational", "required", MATHLIB_BODY, 35,
    ),
    (
        "L-RIGHT-FACTOR", "core_lemma", "critical",
        "Evaluate the polynomial identity at A and use eval_mul_X_sub_C to kill the right factor without assuming evaluation into matrices is multiplicative.",
        "Stage1Instances.THM_M_0041.ObligationTree.RightFactorEvaluationEngine",
        "Evaluation at A of the transported scalar side is the zero matrix.",
        "informational", "required", MATHLIB_BODY, 30,
    ),
    (
        "T-SCALAR-EVAL", "transport", "critical",
        "Rewrite matPolyEquiv of charpoly A times one using matPolyEquiv_smul_one, then use eval_map to recover Polynomial.aeval A A.charpoly.",
        "Stage1Instances.THM_M_0041.ObligationTree.ScalarEvaluationTransportEngine",
        "Polynomial.aeval A A.charpoly = 0.",
        "informational", "required", MATHLIB_BODY, 25,
    ),
    (
        "T-BODY-ASSEMBLE", "terminal", "critical",
        "Compose the adjugate, representation, right-factor, and scalar-evaluation engines into the exact matrix Cayley-Hamilton interface.",
        "Stage1Instances.THM_M_0041.ObligationTree.matrixCayleyHamilton_of_engines",
        "Stage1Instances.THM_M_0041.ObligationTree.MatrixCayleyHamiltonEngine.",
        "informational", "required", "repo:matrixCayleyHamilton_of_engines", 16,
    ),
    (
        "X-SOURCE", "terminal", "high",
        "Pinpoint and independently review the primary theorem, proof, definitions, coefficient assumptions, attribution, and errata against every mathematical node.",
        "primary-source node crosswalk and review pending",
        "Human-source coverage without machine-proof credit.",
        "not_applicable", "required", None, 45,
    ),
    (
        "X-PROVENANCE", "certificate", "critical",
        "Resolve the local conclusion, exact wrapper, terminal Matrix.aeval_self_charpoly body, shared LinearMap aliases, source blobs, revision, imports, and licenses without duplicate credit.",
        "anchor-audit.json plus transitive declaration provenance pending",
        "Body-level provenance and deduplication without proof credit.",
        "informational", "not_applicable", None, 45,
    ),
    (
        "X-TRUST", "certificate", "critical",
        "Audit the exact terminal declaration's transitive axioms, unsafe/oracle boundaries, compiled artifacts, Lean executable, and replay trust closure.",
        "Lean 4.29.0 and mathlib 8a178386 transitive trust closure pending",
        "Release trust inventory without mathematical proof credit.",
        "informational", "not_applicable", None, 45,
    ),
    (
        "X-READABLE", "terminal", "high",
        "Provide and independently review a node-anchored explanation of the adjugate proof and the noncommutative evaluation subtlety.",
        "node-specific readable reconstruction pending",
        "Readable coverage without machine-proof credit.",
        "not_applicable", "required", None, 55,
    ),
    (
        "X-WORKFLOW", "certificate", "high",
        "Bind proof, validation, source/readable review, freshness, revocation, release, and independent-verification task acceptance.",
        "Stage1 workflow receipts pending",
        "Workflow acceptance without mathematical proof credit.",
        "informational", "not_applicable", None, 24,
    ),
)


CHECKED_INTERFACES = {
    oid("S-INTERFACE"), oid("S-CHARPOLY"), oid("S-BOUNDARY"), oid("T-CHARPOLY"),
    oid("C-ADJUGATE"), oid("N-MATPOLY"), oid("L-RIGHT-FACTOR"),
    oid("T-SCALAR-EVAL"), oid("T-BODY-ASSEMBLE"),
}
LEDGERS = {
    oid("ROOT"): {
        "premises": [oid("T-CHARPOLY"), oid("A-MATHLIB-ANCHOR")],
        "inference": "root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton",
        "output": "Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
        "outgoing_use": ["canonical theorem root and release decision"],
    },
    oid("S-INTERFACE"): {
        "premises": ["statement.json expression fingerprint", "Statement.lean elaborated declaration"],
        "inference": "checked statement-gate elaboration with fixed universes and ordered binders",
        "output": "exact R/n/A binder context and aeval conclusion",
        "outgoing_use": [oid("ROOT")],
    },
    oid("S-CHARPOLY"): {
        "premises": ["Matrix.det", "Matrix.scalar n Polynomial.X", "A.map Polynomial.C"],
        "inference": "Stage1Instances.THM_M_0041.characteristicPolynomial definition",
        "output": "det (X I - A.map C) : Polynomial R",
        "outgoing_use": [oid("ROOT"), oid("T-CHARPOLY")],
    },
    oid("S-BOUNDARY"): {
        "premises": ["BoundaryProbe empty-index elaboration", "BoundaryProbe zero-ring elaboration"],
        "inference": "statement mutation and boundary probes reject Nonempty/Nontrivial strengthening",
        "output": "empty n and zero R remain in the universal domain",
        "outgoing_use": [oid("ROOT")],
    },
    oid("S-FOUNDATION"): {
        "premises": ["terminal declaration dependency closure", "Lean executable and compiled imports"],
        "inference": "planned foundation/TCB inclusion check against the selected policy",
        "output": "accepted axioms, TCB inventory, and no-oracle decision",
        "outgoing_use": [oid("ROOT"), oid("A-MATHLIB-ANCHOR")],
    },
    oid("T-CHARPOLY"): {
        "premises": [oid("S-CHARPOLY"), "Matrix.charpoly definition"],
        "inference": "characteristicPolynomialTransport by definitional reduction (rfl)",
        "output": "forall A, characteristicPolynomial A = Matrix.charpoly A",
        "outgoing_use": [oid("ROOT")],
    },
    oid("A-MATHLIB-ANCHOR"): {
        "premises": ["pinned Matrix.aeval_self_charpoly terminal declaration"],
        "inference": "audited exact statement match and terminal-body identity",
        "output": "forall A, Polynomial.aeval A A.charpoly = 0",
        "outgoing_use": [oid("ROOT")],
    },
    oid("C-ADJUGATE"): {
        "premises": ["Matrix.adjugate_mul A.charmatrix", "Matrix.charpoly and charmatrix definitions"],
        "inference": "symmetry of the adjugate determinant identity",
        "output": "A.charpoly * one = adjugate(A.charmatrix) * A.charmatrix",
        "outgoing_use": [oid("N-MATPOLY")],
    },
    oid("N-MATPOLY"): {
        "premises": [oid("C-ADJUGATE")],
        "inference": "apply matPolyEquiv; use map_mul and Matrix.matPolyEquiv_charmatrix",
        "output": "the adjugate identity in Polynomial (Matrix n n R) with right factor X - C A",
        "outgoing_use": [oid("L-RIGHT-FACTOR")],
    },
    oid("L-RIGHT-FACTOR"): {
        "premises": [oid("N-MATPOLY")],
        "inference": "apply Polynomial.eval A and rewrite Polynomial.eval_mul_X_sub_C",
        "output": "Polynomial.eval A (matPolyEquiv (A.charpoly * one)) = 0",
        "outgoing_use": [oid("T-SCALAR-EVAL")],
    },
    oid("T-SCALAR-EVAL"): {
        "premises": [oid("L-RIGHT-FACTOR")],
        "inference": "rewrite matPolyEquiv_smul_one and Polynomial.eval_map",
        "output": "Polynomial.aeval A A.charpoly = 0",
        "outgoing_use": [oid("T-BODY-ASSEMBLE")],
    },
    oid("T-BODY-ASSEMBLE"): {
        "premises": [oid("C-ADJUGATE"), oid("N-MATPOLY"), oid("L-RIGHT-FACTOR"), oid("T-SCALAR-EVAL")],
        "inference": "matrixCayleyHamilton_of_engines consumes the four typed engine interfaces in source order",
        "output": "MatrixCayleyHamiltonEngine",
        "outgoing_use": [oid("A-MATHLIB-ANCHOR")],
    },
    oid("X-SOURCE"): {
        "premises": ["primary 1858 source snapshot", "definition/assumption/errata crosswalk"],
        "inference": "planned independent source-to-node review",
        "output": "pinpoint H classification for every root-relevant mathematical node",
        "outgoing_use": [oid("ROOT"), oid("X-READABLE")],
    },
    oid("X-PROVENANCE"): {
        "premises": ["anchor-audit candidate inventory", "terminal source blob and import graph"],
        "inference": "planned wrapper/body/origin/license resolution and alias deduplication",
        "output": "transitive provenance closure for Matrix.aeval_self_charpoly",
        "outgoing_use": [oid("A-MATHLIB-ANCHOR"), oid("X-TRUST")],
    },
    oid("X-TRUST"): {
        "premises": [oid("X-PROVENANCE"), "machine-derived axiom/dependency report"],
        "inference": "planned foundation, TCB, unsafe/oracle, supply-chain, and replay validation",
        "output": "accepted trust closure for the terminal object",
        "outgoing_use": [oid("ROOT"), oid("X-WORKFLOW")],
    },
    oid("X-READABLE"): {
        "premises": [oid("X-SOURCE"), "all root-relevant proof and transport nodes"],
        "inference": "planned independently reviewed node-by-node reconstruction",
        "output": "R classification and anchored public proof route",
        "outgoing_use": [oid("ROOT"), oid("X-WORKFLOW")],
    },
    oid("X-WORKFLOW"): {
        "premises": ["accepted prerequisite task receipts", oid("X-TRUST"), oid("X-READABLE")],
        "inference": "planned DAG, freshness, revocation, independent-verification, and release checks",
        "output": "dependency-legal workflow and release decision inputs",
        "outgoing_use": [oid("ROOT")],
    },
}
for _identifier, _ledger in LEDGERS.items():
    _ledger["steps"] = [{
        "step_id": f"{_identifier}-STEP-01",
        "premise_ids": _ledger["premises"],
        "inference_or_source": _ledger["inference"],
        "exact_output": _ledger["output"],
        "outgoing_use_ids": _ledger["outgoing_use"],
    }]
SOURCE_NA = {
    oid("S-INTERFACE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"),
    oid("X-TRUST"), oid("X-WORKFLOW"),
}


def edge(edge_id: str, source: str, kind: str, target: str,
         reciprocal: str | None = None) -> dict:
    result = {"edge_id": edge_id, "from": source, "type": kind, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


def graph(edges: list[dict]) -> dict:
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []
    exclusions = {
        oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_independent_review",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_independent_review",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_independent_proof_credit_pending_integration_review",
        oid("X-TRUST"): "trust_overlay_no_independent_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_independent_proof_credit_pending_integration_review",
        oid("C-ADJUGATE"): "imported_terminal_body_internal_step_no_independent_proof_credit",
        oid("N-MATPOLY"): "imported_terminal_body_internal_step_no_independent_proof_credit",
        oid("L-RIGHT-FACTOR"): "imported_terminal_body_internal_step_no_independent_proof_credit",
        oid("T-SCALAR-EVAL"): "imported_terminal_body_internal_step_no_independent_proof_credit",
        oid("T-BODY-ASSEMBLE"): "conditional_imported_body_reconstruction_no_independent_proof_credit",
    }

    for short, kind, risk, claim, target, output, machine, human, body, budget in ROWS:
        identifier = oid(short)
        if identifier in {oid("ROOT"), oid("S-INTERFACE")}:
            fingerprint = f"lean-expression-sha256:{ROOT_EXPRESSION}"
        else:
            fingerprint = "planned:v1:sha256:" + digest(
                [identifier, kind, claim, target, output]
            )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusions.get(identifier),
            "terminal_proof_body_id": body,
        })

        if identifier == oid("ROOT") or identifier == oid("A-MATHLIB-ANCHOR"):
            machine_debt = "M3"
        elif identifier in CHECKED_INTERFACES:
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        if identifier == oid("A-MATHLIB-ANCHOR"):
            provenance = "anchor-audit:M0041-C01-MATHLIB-EXACT"
        elif identifier in {
            oid("C-ADJUGATE"), oid("N-MATPOLY"), oid("L-RIGHT-FACTOR"),
            oid("T-SCALAR-EVAL"),
        }:
            provenance = "pinned-mathlib:Matrix.aeval_self_charpoly-internal-step"
        elif identifier in {oid("T-CHARPOLY"), oid("T-BODY-ASSEMBLE")}:
            provenance = "local-conditional-composition"
        else:
            provenance = "none"
        owned_sources = []
        if identifier in {
            oid("T-CHARPOLY"), oid("C-ADJUGATE"), oid("N-MATPOLY"),
            oid("L-RIGHT-FACTOR"), oid("T-SCALAR-EVAL"), oid("T-BODY-ASSEMBLE"),
        }:
            owned_sources = [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-CHARPOLY")}:
            owned_sources = [f"Stage1_Instances/{THEOREM}/Statement.lean"]
        elif identifier == oid("S-BOUNDARY"):
            owned_sources = [f"Stage1_Instances/{THEOREM}/BoundaryProbe.lean"]

        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": (
                ["S56-M-0041-OBLIGATION-TREE-WORKER-20260713"]
                if identifier in CHECKED_INTERFACES else []
            ),
            "source_crosswalk_id": (
                "not-applicable-pending-review"
                if identifier in SOURCE_NA else "primary-source-node-map-pending"
            ),
            "provenance_id": provenance,
            "foundation_profile": "lean4-foundation-statement-frozen/1.0; proof-specific acceptance pending",
            "tcb_profile": "lean4-mathlib-statement-frozen/1.0; transitive proof closure and replay pending",
            "computation_record": "none; no solver, native oracle, numerical experiment, reflection, or unchecked certificate is credited",
            "step_budget": len(LEDGERS[identifier]["steps"]),
            "semantic_step_ledger": LEDGERS[identifier],
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no accepted proof, source/readability review, root closure, or theorem completion.",
            "task_ids": (
                [ITEM, "S56-M-0041-VALIDATION", "S56-M-0041-RELEASE"]
                if identifier in {oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE")}
                else [ITEM, "S56-M-0041-PROOF"]
                if identifier != oid("X-WORKFLOW")
                else [ITEM, "S56-M-0041-PROOF", "S56-M-0041-VALIDATION", "S56-M-0041-RELEASE"]
            ),
            "owned_sources": owned_sources,
            "owner": "THM-M-0041 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "at master integration and before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "toolchain and dependency pins",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    projection = [{field: row[field] for field in REGISTRY_FIELDS} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0041-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T08:20:00+08:00",
        "freeze_basis": "The exact elaborated expanded-determinant target and immutable anchor audit, expanded along the visible pinned Matrix.aeval_self_charpoly body before assigning any closure credit.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
        },
        "layer_exclusions": {
            "additional_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The proof body is uniform in the coefficient ring and finite index type and performs no case split; empty dimensions and zero rings remain included in S-BOUNDARY.",
            },
            "additional_normalization": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "All representation work is explicit in N-MATPOLY; there is no symmetry, ordering, primitive representative, finite/infinite, or local/global normalization.",
            },
            "computation_and_certificates": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The visible route is proof-producing Lean code with no solver, reflection, native computation, numerical experiment, oracle, or external certificate.",
            },
        },
        "deduplication": {
            "terminal_body_id": MATHLIB_BODY,
            "aliases_without_independent_credit": [
                "Stage1Instances.THM_M_0041_AnchorAudit.exactMathlibAnchor",
                "LinearMap.aeval_self_charpoly",
                "LinearMap.exists_monic_and_aeval_eq_zero",
                "Omega.Zeta.paper_zeta_syntax_trace_linear_recurrence",
            ],
            "special_case_without_root_credit": "Matrix.cayleyHamilton_fin_two",
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility, weight, or target change requires registry version 2 with an append-only old/new ID delta.",
        "obligations": obligations,
        "append_only_delta": [],
        "status_observed_after_freeze": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "root_machine_debt": "M3",
        },
        "status_boundary": "The frozen denominator and typed architecture carry no accepted closure. The exact mathlib route and conditional local compositions remain provisional; H0, M0-W, R0, AUDIT-Z, and theorem completion are open.",
    }

    # The root consumes the transport and exact anchor. Internal proof-body nodes are an expository
    # decomposition of the imported anchor; their single conditional harness consumes all four
    # interfaces but confers no local proof credit.
    proof_pairs = (
        (oid("ROOT"), oid("T-CHARPOLY")),
        (oid("ROOT"), oid("A-MATHLIB-ANCHOR")),
    )
    proof_edges: list[dict] = []
    for parent, child in proof_pairs:
        req = f"REQ-{parent}-{child}"
        comp = f"CMP-{child}-{parent}"
        proof_edges.extend([
            edge(req, parent, "proof_requires", child, comp),
            edge(comp, child, "composes", parent, req),
        ])

    graph_edges = {
        "proof": proof_edges,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "logical_decomposition", oid("S-INTERFACE")),
            edge("REF-ROOT-CHARPOLY", oid("ROOT"), "logical_decomposition", oid("S-CHARPOLY")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ANCHOR-BODY", oid("A-MATHLIB-ANCHOR"), "expository_decomposition", oid("T-BODY-ASSEMBLE")),
            edge("REF-BODY-ADJUGATE", oid("T-BODY-ASSEMBLE"), "expository_decomposition", oid("C-ADJUGATE")),
            edge("REF-BODY-MATPOLY", oid("T-BODY-ASSEMBLE"), "expository_decomposition", oid("N-MATPOLY")),
            edge("REF-BODY-RIGHT-FACTOR", oid("T-BODY-ASSEMBLE"), "expository_decomposition", oid("L-RIGHT-FACTOR")),
            edge("REF-BODY-SCALAR-EVAL", oid("T-BODY-ASSEMBLE"), "expository_decomposition", oid("T-SCALAR-EVAL")),
        ],
        "provenance": [
            edge("SRC-ROOT", oid("ROOT"), "source_map", oid("X-SOURCE")),
            edge("SRC-ADJUGATE", oid("C-ADJUGATE"), "source_map", oid("X-SOURCE")),
            edge("SRC-EVALUATION", oid("L-RIGHT-FACTOR"), "source_map", oid("X-SOURCE")),
            edge("PROV-ANCHOR", oid("X-PROVENANCE"), "provenance_of", oid("A-MATHLIB-ANCHOR")),
            edge("PROV-BODY", oid("X-PROVENANCE"), "provenance_of", oid("T-BODY-ASSEMBLE")),
        ],
        "evidence": [],
        "trust": [
            edge("TRUST-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ANCHOR", oid("A-MATHLIB-ANCHOR"), "trusts", oid("X-TRUST")),
        ],
        "documentation": [
            edge("DOC-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-SOURCE", oid("X-SOURCE"), "documents", oid("T-BODY-ASSEMBLE")),
            edge("DOC-BOUNDARY", oid("S-BOUNDARY"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-BODY-ANCHOR", oid("T-BODY-ASSEMBLE"), "workflow_depends_on", oid("A-MATHLIB-ANCHOR")),
            edge("FLOW-PROV-BODY", oid("X-PROVENANCE"), "workflow_depends_on", oid("T-BODY-ASSEMBLE")),
            edge("FLOW-TRUST-PROV", oid("X-TRUST"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-READABLE-SOURCE", oid("X-READABLE"), "workflow_depends_on", oid("X-SOURCE")),
            edge("FLOW-WORKFLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
        ],
    }
    graphs = {name: graph(graph_edges[name]) for name in GRAPH_NAMES}
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0041-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_direction": "proof_requires runs parent to child and reciprocal composes runs child to parent; support graphs confer no machine closure.",
        "nodes": nodes,
        "graphs": graphs,
        "evidence_endpoint_policy": "No canonical evidence-object node is accepted in this phase. Node evidence_ids reference only the provisional worker receipt; the evidence graph remains empty rather than conflating X-WORKFLOW with that receipt.",
        "workflow_task_graph": {
            "nodes": [
                {"task_id": "S56-M-0041-INTAKE", "phase": "intake", "layer": 0},
                {"task_id": "S56-M-0041-STATEMENT", "phase": "statement", "layer": 1},
                {"task_id": "S56-M-0041-ANCHOR_AUDIT", "phase": "anchor_audit", "layer": 2},
                {"task_id": ITEM, "phase": "obligation_tree", "layer": 3},
                {"task_id": "S56-M-0041-PROOF", "phase": "proof", "layer": 4},
                {"task_id": "S56-M-0041-VALIDATION", "phase": "validation", "layer": 5},
                {"task_id": "S56-M-0041-RELEASE", "phase": "release", "layer": 6},
            ],
            "edges": [
                {"edge_id": "TASK-STATEMENT-INTAKE", "type": "workflow_depends_on", "from": "S56-M-0041-STATEMENT", "to": "S56-M-0041-INTAKE"},
                {"edge_id": "TASK-ANCHOR-STATEMENT", "type": "workflow_depends_on", "from": "S56-M-0041-ANCHOR_AUDIT", "to": "S56-M-0041-STATEMENT"},
                {"edge_id": "TASK-TREE-ANCHOR", "type": "workflow_depends_on", "from": ITEM, "to": "S56-M-0041-ANCHOR_AUDIT"},
                {"edge_id": "TASK-PROOF-TREE", "type": "workflow_depends_on", "from": "S56-M-0041-PROOF", "to": ITEM},
                {"edge_id": "TASK-VALIDATION-PROOF", "type": "workflow_depends_on", "from": "S56-M-0041-VALIDATION", "to": "S56-M-0041-PROOF"},
                {"edge_id": "TASK-RELEASE-VALIDATION", "type": "workflow_depends_on", "from": "S56-M-0041-RELEASE", "to": "S56-M-0041-VALIDATION"},
            ],
            "task_obligation_links": [
                {"task_id": task_id, "obligation_id": node["obligation_id"]}
                for node in nodes for task_id in node["task_ids"]
            ],
        },
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "root_closed": False,
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [
                oid("T-CHARPOLY"), oid("A-MATHLIB-ANCHOR"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"),
                oid("X-WORKFLOW"),
            ],
            "composition_certificates": [
                "Stage1Instances.THM_M_0041.ObligationTree.characteristicPolynomialTransport",
                "Stage1Instances.THM_M_0041.ObligationTree.matrixCayleyHamilton_of_engines",
                "Stage1Instances.THM_M_0041.ObligationTree.root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton",
            ],
            "reason": "The Lean declarations are conditional compositions. No premise engine, imported body, trust/source/readability boundary, or root has an accepted receipt.",
        },
    }

    recipes_list = []
    checked_recipe_ids = {
        oid("S-INTERFACE"), oid("S-CHARPOLY"), oid("S-BOUNDARY"), oid("T-CHARPOLY"),
        oid("C-ADJUGATE"), oid("N-MATPOLY"), oid("L-RIGHT-FACTOR"),
        oid("T-SCALAR-EVAL"), oid("T-BODY-ASSEMBLE"), oid("A-MATHLIB-ANCHOR"), oid("ROOT"),
    }
    declarations_by_id = {
        oid("T-CHARPOLY"): ["Stage1Instances.THM_M_0041.ObligationTree.characteristicPolynomialTransport"],
        oid("T-BODY-ASSEMBLE"): ["Stage1Instances.THM_M_0041.ObligationTree.matrixCayleyHamilton_of_engines"],
        oid("A-MATHLIB-ANCHOR"): [],
        oid("ROOT"): ["Stage1Instances.THM_M_0041.ObligationTree.root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton"],
    }
    for identifier in ids:
        checked = identifier in checked_recipe_ids
        recipes_list.append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains PASS THM-M-0041 obligation tree",
            }],
            "covered_obligation_ids": [identifier],
            "covered_declarations": declarations_by_id.get(identifier, []),
            "coverage_semantics": "provisional_interface_and_architecture_validation" if checked else "open_state_classification_only",
            "closure_credit": False,
        })
    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": recipes_list,
        "status_boundary": "This worker recipe validates structure and conditional composition only; it does not provide E0/E1 or close any obligation.",
    }

    instance = json.loads((HERE / "instance.json").read_text(encoding="utf-8"))
    instance["obligation_registry_hash"] = f"sha256:{denominator}"
    new_owned = [
        "README.md",
        "AnchorAudit.lean", "anchor-audit-receipt.json", "anchor-audit-validation.md",
        "anchor-audit.json", "anchor-audit.md", "check_anchor_audit.py",
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
        "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
    ]
    for name in new_owned:
        if name not in instance["owned_artifacts"]:
            instance["owned_artifacts"].append(name)
        target = f"Stage1_Instances/{THEOREM}/{name}"
        if target not in instance["public_merge_targets"]:
            instance["public_merge_targets"].append(target)
    instance["status_boundary"] = (
        "The exact target, anchor inventory, registry v1, typed graphs, and conditional composition interfaces are self-tested pending dependency-ordered master acceptance. The exact mathlib body remains a provisional M0-W route only. No accepted H0, M0, R0, proof state, AUDIT-Z, or theorem completion is claimed."
    )
    return registry, bundle, recipes, instance


def render(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    registry, bundle, recipes, instance = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
        ("instance.json", instance),
    ):
        (HERE / name).write_text(render(value), encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"generated {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
