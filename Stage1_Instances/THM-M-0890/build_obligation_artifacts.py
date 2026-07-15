#!/usr/bin/env python3
"""Build the frozen THM-M-0890 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0890-OBLIGATION_TREE"
THEOREM = "THM-M-0890"
PREFIX = "M0890"
ROOT_EXPRESSION = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
GRAPH_NAMES = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
STRUCTURE_RECIPE = "VAL-M0890-OBLIGATION-STRUCTURE"
LEAN_RECIPE = "VAL-M0890-OBLIGATION-LEAN"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def exclusion(code: str, justification: str) -> dict[str, str]:
    return {
        "code": code,
        "justification": justification,
        "approval": "pending independent Stage1 integration review",
    }


# Semantic roles and eligibility are frozen without closure status. The final two fields are
# machine and human-source eligibility; readable eligibility is derived below.
ROWS = (
    ("ROOT", "root", "critical", "Prove the exact positive-degree regular-simple-graph Hoffman ratio-bound target.", "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget", "The exact frozen real inequality at every canonical binder.", "required", "required"),
    ("S-TARGET", "definition", "critical", "Preserve the finite nonempty vertex universe, decidable simple graph, natural regular degree, positive-degree premise, casts, and quotient conclusion.", "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget", "The unchanged elaborated root context and conclusion.", "required", "required"),
    ("S-LEAST", "definition", "high", "Freeze the least adjacency eigenvalue as the final entry of mathlib's antitone Hermitian eigenvalues0 enumeration.", "Stage1Instances.THM_M_0890.leastAdjacencyEigenvalue", "The exact real spectral parameter used throughout.", "required", "required"),
    ("S-INDEPENDENCE", "definition", "high", "Freeze indepNum and a maximum independent Finset witness without confusing maximum with merely maximal.", "SimpleGraph.indepNum; MaximumIndependentSetWitnessTarget", "An independent Finset with cardinality exactly indepNum.", "required", "required"),
    ("S-BOUNDARY", "branch", "critical", "Exclude empty carriers and zero-degree regular graphs while retaining degree one, disconnected regular graphs, and repeated least eigenvalues.", "Statement.lean positive-degree and Nonempty boundary", "The exact exhaustive boundary policy of the root.", "required", "required"),
    ("S-TRANSPORT", "transport", "high", "Relate a maximum-independent-set division-free estimate to indepNum and then transport through a strictly positive denominator to the canonical quotient.", "divisionFree_of_maximumEstimate; root_of_ratio_assembly", "Checked one-way transports with no duplicate root credit.", "required", "not_applicable"),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical finite spectral infrastructure, choice, quotient soundness, imports, compiled artifacts, and the no-oracle computation policy.", "planned transitive foundation and TCB report", "An accepted foundation and trust boundary.", "required", "not_applicable"),
    ("N-MAX-WITNESS", "normalization", "high", "Expose a maximum independent Finset and retain both independence and exact indepNum cardinality.", "MaximumIndependentSetWitnessTarget", "A canonical finite witness for the source principal-submatrix argument.", "required", "required"),
    ("N-LEAST-MIN", "normalization", "critical", "Prove that the final eigenvalues0 entry is no greater than every adjacency eigenvalue and align its index with the spectral decomposition used by the proof.", "planned least-index/eigenbasis ordering theorem", "The spectral minimality property of leastAdjacencyEigenvalue.", "required", "required"),
    ("L-LEAST-NEGATIVE", "core_lemma", "critical", "Use positive regular degree and the zero-diagonal adjacency spectrum to prove the least adjacency eigenvalue is strictly negative.", "planned leastAdjacencyEigenvalue G < 0 theorem", "Strict negativity of the least eigenvalue.", "required", "required"),
    ("N-DENOMINATOR", "normalization", "critical", "Combine positive degree with strict least-eigenvalue negativity to prove 0 < k - lambda_min.", "DenominatorPositiveTarget", "A legal positive divisor for the final transport.", "required", "required"),
    ("L-REGULAR-ONES", "core_lemma", "high", "Show that the real adjacency matrix sends the all-ones vector to k times that vector.", "SimpleGraph.adjMatrix_mulVec_const_apply_of_regular", "The regular all-ones eigenpair.", "required", "required"),
    ("L-ONES-ORTHOGONAL", "core_lemma", "critical", "Describe the action of the all-ones matrix on the all-ones line and its orthogonal complement.", "planned J eigenspace and orthogonal-complement package", "The two spectral actions needed for the Hoffman shift.", "required", "required"),
    ("C-HOFFMAN-MATRIX", "construction", "critical", "Construct E = A - ((k-lambda_min)/n) J - lambda_min I with every cast and nonzero order proof explicit.", "planned exact Matrix V V Real definition", "The source Hoffman matrix E.", "required", "required"),
    ("L-COMMON-EIGENBASIS", "bridge", "critical", "Build or import an exact common eigenbasis for A and J from the regular all-ones eigenpair and the orthogonal complement.", "planned common eigenbasis bridge", "A basis in which every eigenvalue of E is explicit.", "required", "required"),
    ("L-HOFFMAN-PSD", "core_lemma", "critical", "Use least-eigenvalue minimality and the common eigenbasis to prove E is positive semidefinite.", "planned Matrix.PosSemidef E theorem", "Positive semidefiniteness of the full Hoffman matrix.", "required", "required"),
    ("C-PRINCIPAL", "construction", "high", "Restrict E along the subtype inclusion of the selected maximum independent Finset.", "Matrix.submatrix E Subtype.val Subtype.val", "The principal matrix indexed by the independent set.", "required", "required"),
    ("L-PSD-PRINCIPAL", "bridge", "high", "Transport positive semidefiniteness to the independent-set principal submatrix.", "Matrix.PosSemidef.submatrix", "Positive semidefiniteness of the restricted matrix.", "required", "required"),
    ("L-INDEPENDENT-ZERO", "core_lemma", "high", "Use independence to prove the restricted adjacency block is zero entrywise.", "planned adjacency-submatrix zero theorem from SimpleGraph.IsIndepSet", "Elimination of the adjacency term on the selected vertices.", "required", "required"),
    ("T-RESTRICTED-FORM", "transport", "critical", "Simplify the restricted Hoffman matrix to -((k-lambda_min)/n) J_alpha - lambda_min I_alpha.", "planned exact principal-submatrix equality", "The explicit alpha-by-alpha source matrix.", "required", "required"),
    ("C-ONES-VECTOR", "construction", "normal", "Construct the finitely supported all-ones vector on the finite independent-set subtype.", "planned Finsupp indicator vector", "A legal quadratic-form test vector.", "required", "required"),
    ("L-QUADRATIC-EVAL", "core_lemma", "critical", "Evaluate the restricted positive-semidefinite quadratic form on the all-ones vector.", "planned exact finite-sum evaluation", "0 <= alpha * (-lambda_min - alpha*(k-lambda_min)/n).", "required", "required"),
    ("B-ALPHA-POSITIVE", "branch", "high", "Prove the maximum independent-set cardinality is positive from Nonempty V, separating rather than hiding the zero-alpha division case.", "planned 0 < indepNum theorem", "A positive alpha factor for scalar cancellation.", "required", "required"),
    ("L-SCALAR-ESTIMATE", "core_lemma", "critical", "Use positive alpha and graph order to cancel the quadratic-form factors and obtain the division-free maximum-independent-set estimate.", "MaximumIndependentSetEstimateTarget", "alpha*(k-lambda_min) <= n*(-lambda_min).", "required", "required"),
    ("T-DIVISION-FREE", "terminal", "critical", "Transport the selected maximum witness and scalar estimate to the indepNum division-free inequality.", "DivisionFreeInequalityTarget", "The exact numerator inequality at the canonical root binders.", "required", "required"),
    ("T-ASSEMBLE", "terminal", "critical", "Pair denominator positivity and the division-free inequality as the exact terminal package consumed by root transport.", "RatioAssemblyTarget", "DenominatorPositiveTarget and DivisionFreeInequalityTarget.", "required", "required"),
    ("X-MATHLIB", "certificate", "high", "Record the audit and provenance boundary for the exact pinned independent-set, regular adjacency, Hermitian spectrum, submatrix, and positive-semidefinite declarations used by future proof bodies.", "mathlib support-interface inventory in anchor-audit.json", "Classified imported-interface governance without semantic proof credit.", "not_applicable", "not_applicable"),
    ("X-SOURCE", "terminal", "critical", "Map every definition, matrix transition, scalar inequality, historical correction, and omitted denominator fact to Haemers Theorem 1 and independent review.", "Haemers-2021-Theorem-1-node-map-v1", "Human-source evidence without machine proof credit.", "not_applicable", "required"),
    ("X-PROVENANCE", "certificate", "critical", "Bind every future terminal body, wrapper, import, revision, license, source slice, and transitive declaration origin.", "planned content-addressed provenance closure", "Release provenance without semantic proof credit.", "informational", "not_applicable"),
    ("X-EVIDENCE", "certificate", "high", "Bind structured node recipes, outputs, fingerprints, and receipts to immutable source snapshots.", "planned node evidence closure", "Evidence coverage without semantic proof credit.", "informational", "not_applicable"),
    ("X-TRUST", "certificate", "critical", "Close executable, imported-olean, axiom, unsafe/oracle, computation, reproducibility, and independent-verification boundaries.", "planned transitive trust and TCB closure", "Release trust evidence without semantic proof credit.", "informational", "not_applicable"),
    ("X-READABLE", "terminal", "high", "Produce and independently review a complete node-anchored reconstruction of the spectral and scalar argument.", "planned readable reconstruction", "Readable coverage without machine proof credit.", "not_applicable", "not_applicable"),
    ("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent-verification tasks.", "planned Stage1 workflow receipts", "Workflow acceptance without proof credit.", "informational", "not_applicable"),
)


CHECKED_INTERFACES = {
    oid("ROOT"), oid("S-INDEPENDENCE"), oid("S-TRANSPORT"), oid("N-MAX-WITNESS"),
    oid("N-DENOMINATOR"), oid("L-SCALAR-ESTIMATE"), oid("T-DIVISION-FREE"), oid("T-ASSEMBLE"),
}
EXACT_INTERFACE_TARGETS = {
    oid("ROOT"): "lean-expression-sha256:" + ROOT_EXPRESSION,
    oid("S-TARGET"): "lean-expression-sha256:" + ROOT_EXPRESSION,
}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    row_by_id: dict[str, tuple] = {}
    for short, kind, risk, claim, target, output, machine, human_source in ROWS:
        identifier = oid(short)
        row_by_id[identifier] = (short, kind, risk, claim, target, output, machine, human_source)
        fingerprint = EXACT_INTERFACE_TARGETS.get(
            identifier,
            "planned:v1:sha256:" + digest([identifier, kind, claim, target, output]),
        )
        excluded = None
        if machine != "required" or human_source != "required":
            if machine == "required":
                excluded = exclusion(
                    "formal_or_import_boundary_not_human_claim",
                    "This formal transport, foundation, or imported-interface boundary is not a separate human mathematical claim.",
                )
            elif identifier == oid("X-SOURCE"):
                excluded = exclusion(
                    "human_source_boundary_only",
                    "This obligation carries human-source review and never receives machine proof credit.",
                )
            elif identifier == oid("X-READABLE"):
                excluded = exclusion(
                    "readability_boundary_only",
                    "This obligation carries readable reconstruction and never receives machine or source proof credit.",
                )
            else:
                excluded = exclusion(
                    "assurance_overlay_no_proof_credit",
                    "This provenance, evidence, trust, or workflow overlay is informational for proof coverage.",
                )
        readable = "not_applicable" if identifier in {
            oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"), oid("X-WORKFLOW")
        } else "required"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-WORKFLOW")},
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": readable,
            "risk_class": risk,
            "exclusion_reason": excluded,
            "terminal_proof_body_id": None,
        })

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
        "registry_id": "THM-M-0890-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-15T15:59:29+08:00",
        "freeze_basis": "The exact elaborated positive-degree target and Haemers Theorem 1's all-ones, Hoffman-matrix, principal-submatrix, and scalar-estimate architecture, with omitted denominator work expanded. Eligibility follows semantic roles, not candidate availability or closure.",
        "freeze_order_boundary": "ROWS contains no observed proof status; its canonical ten-field projection is hashed before status_observed_after_freeze is attached.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
            "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
        },
        "mandatory_layer_analysis": {
            "S": [oid(x) for x in ("S-TARGET", "S-LEAST", "S-INDEPENDENCE", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION")],
            "N": [oid(x) for x in ("N-MAX-WITNESS", "N-LEAST-MIN", "N-DENOMINATOR")],
            "B": [oid(x) for x in ("S-BOUNDARY", "B-ALPHA-POSITIVE")],
            "C": [oid(x) for x in ("C-HOFFMAN-MATRIX", "C-PRINCIPAL", "C-ONES-VECTOR")],
            "L": [oid(x) for x in ("L-LEAST-NEGATIVE", "L-REGULAR-ONES", "L-ONES-ORTHOGONAL", "L-COMMON-EIGENBASIS", "L-HOFFMAN-PSD", "L-PSD-PRINCIPAL", "L-INDEPENDENT-ZERO", "L-QUADRATIC-EVAL", "L-SCALAR-ESTIMATE")],
            "X": [oid(x) for x in ("X-MATHLIB", "X-SOURCE", "X-PROVENANCE", "X-EVIDENCE", "X-TRUST", "X-READABLE", "X-WORKFLOW")],
            "T": [oid(x) for x in ("T-RESTRICTED-FORM", "T-DIVISION-FREE", "T-ASSEMBLE", "ROOT")],
            "not_applicable_layers": [],
        },
        "layer_exclusions": {
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected route is symbolic. No solver, native evaluator, floating-point eigensolver, external oracle, experiment, or unchecked certificate is used; finite sums remain kernel-proof obligations.",
                "reviewer": "independent Stage1 integration lane",
            },
            "additional_mathematical_case_splits": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The only material scalar split is isolated as B-ALPHA-POSITIVE; connectedness, eigenvalue multiplicity, and equality cases do not branch the selected inequality proof.",
                "reviewer": "independent spectral-graph-theory reviewer",
            },
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility change, edge-role change, risk change, or terminal-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_machine_classification": "M3_no_exact_proof_candidate",
            "candidate_evidence_level": "E3_exact_statement_and_support_interfaces_only",
            "candidate_closure_credit": False,
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope, eligibility, and denominators only. Conditional interface checks close no mathematical obligation; H1/M3/R4, AUDIT-Z, and theorem completion do not change.",
    }

    # Exact checked composition occurs only at the maximum-witness wrapper and top proof spine.
    # Every deeper mathematical relation is explicitly an unverified source decomposition.
    proof_pairs = (
        (oid("ROOT"), oid("T-ASSEMBLE"), "composes"),
        (oid("T-ASSEMBLE"), oid("N-DENOMINATOR"), "composes"),
        (oid("T-ASSEMBLE"), oid("T-DIVISION-FREE"), "composes"),
        (oid("T-DIVISION-FREE"), oid("N-MAX-WITNESS"), "composes"),
        (oid("T-DIVISION-FREE"), oid("L-SCALAR-ESTIMATE"), "composes"),
        (oid("N-DENOMINATOR"), oid("L-LEAST-NEGATIVE"), "logical_decomposition"),
        (oid("N-DENOMINATOR"), oid("S-BOUNDARY"), "logical_decomposition"),
        (oid("L-LEAST-NEGATIVE"), oid("N-LEAST-MIN"), "logical_decomposition"),
        (oid("L-LEAST-NEGATIVE"), oid("L-REGULAR-ONES"), "logical_decomposition"),
        (oid("L-SCALAR-ESTIMATE"), oid("L-QUADRATIC-EVAL"), "logical_decomposition"),
        (oid("L-SCALAR-ESTIMATE"), oid("B-ALPHA-POSITIVE"), "logical_decomposition"),
        (oid("L-SCALAR-ESTIMATE"), oid("S-BOUNDARY"), "logical_decomposition"),
        (oid("L-QUADRATIC-EVAL"), oid("L-PSD-PRINCIPAL"), "logical_decomposition"),
        (oid("L-QUADRATIC-EVAL"), oid("T-RESTRICTED-FORM"), "logical_decomposition"),
        (oid("L-QUADRATIC-EVAL"), oid("C-ONES-VECTOR"), "logical_decomposition"),
        (oid("L-PSD-PRINCIPAL"), oid("L-HOFFMAN-PSD"), "logical_decomposition"),
        (oid("L-PSD-PRINCIPAL"), oid("C-PRINCIPAL"), "logical_decomposition"),
        (oid("T-RESTRICTED-FORM"), oid("C-PRINCIPAL"), "logical_decomposition"),
        (oid("T-RESTRICTED-FORM"), oid("L-INDEPENDENT-ZERO"), "logical_decomposition"),
        (oid("T-RESTRICTED-FORM"), oid("C-HOFFMAN-MATRIX"), "logical_decomposition"),
        (oid("C-PRINCIPAL"), oid("N-MAX-WITNESS"), "logical_decomposition"),
        (oid("L-HOFFMAN-PSD"), oid("C-HOFFMAN-MATRIX"), "logical_decomposition"),
        (oid("L-HOFFMAN-PSD"), oid("L-COMMON-EIGENBASIS"), "logical_decomposition"),
        (oid("L-HOFFMAN-PSD"), oid("N-LEAST-MIN"), "logical_decomposition"),
        (oid("L-COMMON-EIGENBASIS"), oid("L-REGULAR-ONES"), "logical_decomposition"),
        (oid("L-COMMON-EIGENBASIS"), oid("L-ONES-ORTHOGONAL"), "logical_decomposition"),
        (oid("B-ALPHA-POSITIVE"), oid("N-MAX-WITNESS"), "logical_decomposition"),
    )
    proof_edges: list[dict] = []
    children: dict[str, list[str]] = {}
    for parent, child, reverse_type in proof_pairs:
        req_id = f"REQ-{parent}-{child}"
        reverse_id = f"{'CMP' if reverse_type == 'composes' else 'DEC'}-{child}-{parent}"
        proof_edges.extend((
            {"edge_id": req_id, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": reverse_id},
            {"edge_id": reverse_id, "from": child, "type": reverse_type, "to": parent, "reciprocal_edge_id": req_id},
        ))
        children.setdefault(parent, []).append(child)

    refinement_edges = [
        {"edge_id": "REF-ROOT-TARGET", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-TARGET")},
        {"edge_id": "REF-TARGET-LEAST", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-LEAST")},
        {"edge_id": "REF-TARGET-INDEPENDENCE", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-INDEPENDENCE")},
        {"edge_id": "REF-TARGET-BOUNDARY", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-BOUNDARY")},
        {"edge_id": "REF-TARGET-TRANSPORT", "from": oid("S-TARGET"), "type": "transports", "to": oid("S-TRANSPORT")},
        {"edge_id": "REF-TARGET-FOUNDATION", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-FOUNDATION")},
    ]

    source_required = [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required" and r["obligation_id"] != oid("X-SOURCE")]
    provenance_edges = [
        {"edge_id": f"SOURCE-{identifier}", "from": identifier, "type": "source_map", "to": oid("X-SOURCE")}
        for identifier in source_required
    ]
    provenance_edges += [
        {"edge_id": f"IMPORT-AUDIT-{identifier}", "from": oid("X-MATHLIB"), "type": "provenance_of", "to": identifier}
        for identifier in (
            oid("S-INDEPENDENCE"), oid("N-LEAST-MIN"), oid("L-REGULAR-ONES"),
            oid("L-PSD-PRINCIPAL"), oid("L-COMMON-EIGENBASIS"),
        )
    ]
    # No accepted node evidence or terminal-body provenance exists yet. Keep those graph families
    # empty rather than turning planned assurance overlays into evidence_for/provenance_of claims.
    evidence_edges: list[dict] = []
    trust_edges = [
        {"edge_id": "TRUST-ROOT-FOUNDATION", "from": oid("ROOT"), "type": "trusts", "to": oid("S-FOUNDATION")},
        {"edge_id": "TRUST-ROOT-BOUNDARY", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TRUST")},
        {"edge_id": "TRUST-PROVENANCE", "from": oid("X-PROVENANCE"), "type": "trusts", "to": oid("X-TRUST")},
        {"edge_id": "TRUST-EVIDENCE", "from": oid("X-EVIDENCE"), "type": "trusts", "to": oid("X-TRUST")},
    ]
    documentation_edges = [
        {"edge_id": f"DOCUMENT-{identifier}", "from": oid("X-READABLE"), "type": "documents", "to": identifier}
        for identifier in ids if identifier != oid("X-READABLE")
    ]
    workflow_nodes = [
        "S56-M-0890-ANCHOR_AUDIT", ITEM, "S56-M-0890-PROOF",
        "S56-M-0890-VALIDATION", "S56-M-0890-RELEASE",
    ]
    workflow_edges = [
        {"edge_id": "FLOW-TREE-ANCHOR", "from": ITEM, "type": "workflow_depends_on", "to": "S56-M-0890-ANCHOR_AUDIT"},
        {"edge_id": "FLOW-PROOF-TREE", "from": "S56-M-0890-PROOF", "type": "workflow_depends_on", "to": ITEM},
        {"edge_id": "FLOW-VALIDATION-PROOF", "from": "S56-M-0890-VALIDATION", "type": "workflow_depends_on", "to": "S56-M-0890-PROOF"},
        {"edge_id": "FLOW-RELEASE-VALIDATION", "from": "S56-M-0890-RELEASE", "type": "workflow_depends_on", "to": "S56-M-0890-VALIDATION"},
    ]

    checked_source = "Stage1_Instances/THM-M-0890/ObligationTree.lean"
    checked_targets = {
        oid("S-INDEPENDENCE"): "MaximumIndependentSetWitnessTarget",
        oid("S-TRANSPORT"): "divisionFree_of_maximumEstimate",
        oid("N-MAX-WITNESS"): "MaximumIndependentSetWitnessTarget",
        oid("N-DENOMINATOR"): "DenominatorPositiveTarget",
        oid("L-SCALAR-ESTIMATE"): "MaximumIndependentSetEstimateTarget",
        oid("T-DIVISION-FREE"): "DivisionFreeInequalityTarget",
        oid("T-ASSEMBLE"): "RatioAssemblyTarget",
    }
    source_locators = {
        oid("ROOT"): "Haemers-2021:Theorem-1:formula-1",
        oid("L-REGULAR-ONES"): "Haemers-2021:Theorem-1-proof:A-one-equals-k-one",
        oid("C-HOFFMAN-MATRIX"): "Haemers-2021:Theorem-1-proof:E-definition",
        oid("L-HOFFMAN-PSD"): "Haemers-2021:Theorem-1-proof:E-positive-semidefinite",
        oid("C-PRINCIPAL"): "Haemers-2021:Theorem-1-proof:E-alpha-principal-submatrix",
        oid("L-PSD-PRINCIPAL"): "Haemers-2021:Theorem-1-proof:E-alpha-positive-semidefinite",
        oid("T-RESTRICTED-FORM"): "Haemers-2021:Theorem-1-proof:E-alpha-formula",
        oid("L-QUADRATIC-EVAL"): "Haemers-2021:Theorem-1-proof:scalar-inequality",
        oid("L-SCALAR-ESTIMATE"): "Haemers-2021:Theorem-1-proof:final-rearrangement",
        oid("X-SOURCE"): "arXiv:2102.05529v2:pp1-2:Section-2:Theorem-1",
    }
    nodes = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        short, kind, risk, claim, target, output, machine, human_source = row_by_id[identifier]
        checked = identifier in CHECKED_INTERFACES
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if identifier in {oid("ROOT"), oid("S-TARGET")} else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if human_source == "not_applicable" else "haemers-2021-theorem1-node-map-v1-pending-independent-review",
            "provenance_id": "conditional-local-interface:v1" if checked else "none",
            "foundation_profile": "lean4-mathlib-classical/v1-pending-transitive-review",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/v1-pending-release-closure",
            "computation_record": "none credited; all eigenvalue, matrix, and finite-sum work requires kernel proof",
            "step_budget": 85 if risk == "critical" else 55 if risk == "high" else 35,
            "semantic_step_ledger": [{
                "step_id": f"STEP-{identifier}-1",
                "premise_ids": children.get(identifier, ["frozen-formal-context"]),
                "inference": claim,
                "source_locator": source_locators.get(identifier, "architecture:v1:" + identifier),
                "output": output,
                "outgoing_use": "Consumed only by declared proof/refinement edges; no closure follows from this ledger.",
            }],
            "public_readable_target": f"Stage1_Instances/THM-M-0890/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": LEAN_RECIPE if checked else STRUCTURE_RECIPE,
            "status_boundary": "Open architecture obligation or checked conditional interface only; no M0, accepted proof, H0, or R0 credit.",
            "task_ids": [ITEM],
            "owned_sources": [f"{checked_source}#{checked_targets[identifier]}"] if identifier in checked_targets else [],
            "owner": "THM-M-0890 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": None,
                "review_due": "before any proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation registry", "typed edges", "source map", "toolchain"],
                "revocation_state": "not-accepted",
            },
        })

    def graph(edges: list[dict]) -> dict:
        incoming: dict[str, list[str]] = {}
        outgoing: dict[str, list[str]] = {}
        for edge in edges:
            outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
            incoming.setdefault(edge["to"], []).append(edge["edge_id"])
        return {"edges": edges, "out": outgoing, "in": incoming}

    obligation_by_id = {row["obligation_id"]: row for row in obligations}

    def certificate(name: str, parent: str, child_ids: list[str], declaration: str) -> dict:
        return {
            "certificate_id": name,
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
            "required_child_ids": child_ids,
            "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in child_ids},
            "checked_declaration": declaration,
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        }

    composition_certificates = [
        certificate("COMP-M0890-ROOT", oid("ROOT"), [oid("T-ASSEMBLE")], "Stage1Instances.THM_M_0890_Obligations.root_of_ratio_assembly"),
        certificate("COMP-M0890-T-ASSEMBLE", oid("T-ASSEMBLE"), [oid("N-DENOMINATOR"), oid("T-DIVISION-FREE")], "Stage1Instances.THM_M_0890_Obligations.assembly_of_children"),
        certificate("COMP-M0890-T-DIVISION-FREE", oid("T-DIVISION-FREE"), [oid("N-MAX-WITNESS"), oid("L-SCALAR-ESTIMATE")], "Stage1Instances.THM_M_0890_Obligations.divisionFree_of_maximumEstimate"),
    ]
    certificate_parents = {row["parent_obligation_id"] for row in composition_certificates}
    unverified_plans = [
        {
            "plan_id": f"DECOMP-{parent}",
            "parent_obligation_id": parent,
            "planned_child_ids": child_ids,
            "source_declaration": "Haemers 2021 Theorem 1 proof architecture plus explicit formal denominator and scalar-boundary work",
            "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
            "required_future_certificate": "An exact Lean abstract-child harness must bind these fingerprints and consume every child before parent closure.",
        }
        for parent, child_ids in children.items() if parent not in certificate_parents
    ]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_version": 1,
        "registry_denominator_sha256": denominator,
        "root_node_id": f"{THEOREM}-ROOT",
        "workflow_task_nodes": workflow_nodes,
        "nodes": nodes,
        "graphs": {
            "proof": graph(proof_edges),
            "refinement": graph(refinement_edges),
            "provenance": graph(provenance_edges),
            "evidence": graph(evidence_edges),
            "trust": graph(trust_edges),
            "documentation": graph(documentation_edges),
            "workflow": graph(workflow_edges),
        },
        "composition_certificates": composition_certificates,
        "unverified_decomposition_plans": unverified_plans,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": sorted(identifier for identifier in set(ids) if identifier not in children and obligation_by_id[identifier]["machine_eligibility"] == "required"),
            "remaining_machine_root_cut_set": [oid("N-DENOMINATOR"), oid("L-SCALAR-ESTIMATE")],
            "remaining_release_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"), "master acceptance"],
            "candidate_evidence": "E3 exact-statement and support-interface evidence only; no exact root proof candidate was located.",
            "reason": "Only maximum-witness and top-spine conditional composition are checked. Every mathematical premise remains open and every deeper source relation requires a future exact certificate.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": STRUCTURE_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0890/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 120,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0890 obligation tree"}],
                "covered_obligation_ids": ids,
                "covered_declarations": [],
                "coverage_boundary": "Checks registry, schemas, graph semantics, source mappings, and open state only; supplies no kernel proof closure.",
            },
            {
                "recipe_id": LEAN_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", "Stage1_Instances/THM-M-0890/check_obligation_tree.py", "--run-lean"],
                "env_allowlist": {},
                "timeout_seconds": 240,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains Lean composition: pass and no sorryAx"}],
                "covered_obligation_ids": sorted(CHECKED_INTERFACES),
                "covered_declarations": [
                    "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget",
                    "Stage1Instances.THM_M_0890_Obligations.MaximumIndependentSetWitnessTarget",
                    "Stage1Instances.THM_M_0890_Obligations.MaximumIndependentSetEstimateTarget",
                    "Stage1Instances.THM_M_0890_Obligations.DenominatorPositiveTarget",
                    "Stage1Instances.THM_M_0890_Obligations.DivisionFreeInequalityTarget",
                    "Stage1Instances.THM_M_0890_Obligations.RatioAssemblyTarget",
                    "Stage1Instances.THM_M_0890_Obligations.maximumIndependentSetWitness_checked",
                    "Stage1Instances.THM_M_0890_Obligations.divisionFree_of_maximumEstimate",
                    "Stage1Instances.THM_M_0890_Obligations.assembly_of_children",
                    "Stage1Instances.THM_M_0890_Obligations.root_of_ratio_assembly",
                    "Stage1Instances.THM_M_0890_Obligations.root_of_children",
                ],
                "coverage_boundary": "Kernel-checks exact conditional interfaces and composition only. It supplies none of the spectral, positive-semidefinite, denominator, or scalar premises and closes no obligation.",
            },
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
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
