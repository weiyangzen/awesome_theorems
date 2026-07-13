#!/usr/bin/env python3
"""Build the frozen THM-M-0043 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0043-OBLIGATION_TREE"
THEOREM = "THM-M-0043"
PREFIX = "M0043"
ROOT_EXPRESSION = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_BLOB = "393e4c75ddc778f12a3b02e3fb1ef19f653cd76a"
GRAPH_NAMES = (
    "proof",
    "refinement",
    "provenance",
    "evidence",
    "trust",
    "documentation",
    "workflow",
)


def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


# Architecture comes from the exact statement and the visible Atlas/mathlib route. No closure
# status occurs in this table; status is attached only after the denominator has been computed.
ROWS = (
    ("ROOT", "root", "critical", "Prove the exact nonempty finite complex normal-matrix unitary diagonalization target.", "Stage1Instances.THM_M_0043.SpectralTheoremTarget", "The exact frozen spectral-theorem proposition.", "required", "required", None),
    ("S-INTERFACE", "definition", "critical", "Preserve the ordered finite, decidable, nonempty, matrix, and normality binders and the exact existential equation.", "Stage1Instances.THM_M_0043.SpectralTheoremTarget", "The exact domain, antecedent, witnesses, and equality orientation.", "required", "not_applicable", None),
    ("S-BOUNDARY", "branch", "high", "Exclude only the empty index type while retaining zero, identity, repeated-eigenvalue, and singular normal matrices.", "boundary policy of SpectralTheoremTarget", "An exhaustive policy for the frozen degenerate cases.", "required", "required", None),
    ("S-ENCODINGS", "transport", "high", "Relate subtype unitary witnesses, explicit unitary membership, and conjugated-diagonal orientation without changing the claim.", "spectralTheoremTarget_iff_explicitUnitaryMembershipTarget and spectralTheoremTarget_iff_conjugatedDiagonalTarget", "Two checked iff transports with no duplicate root credit.", "required", "not_applicable", "local:Stage1_Instances/THM-M-0043/Statement.lean#statement-transports"),
    ("S-FOUNDATION", "certificate", "critical", "Audit logic, choice, quotient soundness, kernel, imports, computation policy, and transitive trusted code.", "planned transitive foundation and TCB report", "An accepted foundation, trust, and no-oracle boundary.", "required", "not_applicable", None),
    ("N-NORMAL-COMMUTE", "normalization", "high", "Unfold IsStarNormal into commutation of A with its conjugate transpose.", "IsStarNormal.star_comm_self and star_eq_conjTranspose", "A.conjTranspose * A = A * A.conjTranspose.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hN"),
    ("C-HERMITIAN-PARTS", "construction", "critical", "Construct the Hermitian real and imaginary parts H=(A+A*)/2 and K=(-i/2)(A-A*).", "Atlas H and K definitions", "Two matrices whose complex combination reconstructs A.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:H+K"),
    ("L-H-HERMITIAN", "core_lemma", "high", "Prove that the constructed real part H is Hermitian.", "Matrix.IsHermitian H", "A symmetric linear operator associated to H.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hH_herm"),
    ("L-K-HERMITIAN", "core_lemma", "high", "Prove that the constructed imaginary part K is Hermitian.", "Matrix.IsHermitian K", "A symmetric linear operator associated to K.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hK_herm"),
    ("T-M-RECONSTRUCT", "transport", "high", "Reconstruct A as H + i scalar K entrywise.", "A = H + Complex.I smul K", "The matrix equality consumed by operator decomposition.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hA_eq"),
    ("L-HK-COMMUTE", "core_lemma", "critical", "Use normality to prove that H and K commute under matrix multiplication.", "H * K = K * H", "Commutation of the two Hermitian matrix parts.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hHK"),
    ("T-LINEAR-COMMUTE", "transport", "high", "Transport matrix commutation to the associated Euclidean linear maps.", "Commute (Matrix.toEuclideanLin H) (Matrix.toEuclideanLin K)", "The exact hypothesis for the joint-eigenspace theorem.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hcomm"),
    ("C-JOINT-EIGENSPACE", "construction", "critical", "Define the intersections W(lambda,mu) of eigenspaces of the two symmetric operators.", "fun p => eigenspace (toEuclideanLin H) p.2 inf eigenspace (toEuclideanLin K) p.1", "The indexed family of joint eigenspaces.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:W"),
    ("L-JOINT-DECOMP", "bridge", "critical", "Obtain that the full joint eigenspace family is an internal direct sum.", "LinearMap.IsSymmetric.directSum_isInternal_of_commute", "Internal direct-sum coverage over all eigenvalue pairs.", "required", "required", f"mathlib:{MATHLIB_REVISION}:LinearMap.IsSymmetric.directSum_isInternal_of_commute"),
    ("L-JOINT-ORTHOGONAL", "bridge", "critical", "Obtain pairwise orthogonality of distinct joint eigenspaces.", "LinearMap.IsSymmetric.orthogonalFamily_eigenspace_inf_eigenspace", "An orthogonal family indexed by eigenvalue pairs.", "required", "required", f"mathlib:{MATHLIB_REVISION}:LinearMap.IsSymmetric.orthogonalFamily_eigenspace_inf_eigenspace"),
    ("L-FINITE-EIGENVALUES", "bridge", "high", "Use finite-dimensional symmetric-operator spectra to make the nonzero joint-eigenspace subtype finite.", "Eigenvalues and Fintype.ofFinite", "A finite index type for nonzero joint eigenspaces.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:Finite-subtype"),
    ("B-NONZERO-SUBTYPE", "branch", "high", "Restrict the joint family to exactly those eigenspaces not equal to bottom and prove this loses no span.", "iSup_ne_bot_subtype W", "An internal direct sum over nonzero joint eigenspaces only.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hdecomp-prime"),
    ("L-SUBORDINATE-BASIS", "bridge", "critical", "Choose an orthonormal basis subordinate to the finite orthogonal internal direct sum.", "DirectSum.IsInternal.subordinateOrthonormalBasis", "An orthonormal basis whose vectors lie in assigned joint eigenspaces.", "required", "required", f"mathlib:{MATHLIB_REVISION}:DirectSum.IsInternal.subordinateOrthonormalBasis"),
    ("C-BASIS-REINDEX", "construction", "high", "Reindex the subordinate basis from Fin (card n) back to n.", "OrthonormalBasis.reindex (Fintype.equivFin n).symm", "An orthonormal basis indexed by the canonical matrix type n.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:basis"),
    ("T-OPERATOR-DECOMP", "transport", "high", "Transport A=H+iK to equality of their associated Euclidean linear maps.", "toEuclideanLin A = toEuclideanLin H + Complex.I smul toEuclideanLin K", "The operator equation used on every basis vector.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hA_op"),
    ("C-EIGENVALUES", "construction", "high", "Define each eigenvalue as the H eigenvalue plus i times the K eigenvalue assigned to its joint eigenspace.", "Atlas ev definition", "A diagonal-entry function ev : n -> Complex.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:ev"),
    ("L-BASIS-EIGENVECTORS", "core_lemma", "critical", "Show every chosen basis vector is an eigenvector of A with its constructed eigenvalue.", "forall j, toEuclideanLin A (basis j) = ev j smul basis j", "Pointwise eigenvector equations for the full orthonormal basis.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:hMbasis"),
    ("L-UNITARY-BASIS", "bridge", "critical", "Turn a change between orthonormal bases into membership in the matrix unitary group.", "OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary", "The unitary-membership proof for the basis matrix.", "required", "required", f"mathlib:{MATHLIB_REVISION}:OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary"),
    ("C-UNITARY-MATRIX", "construction", "critical", "Construct the basis matrix P and package its unitary membership.", "(EuclideanSpace.basisFun n Complex).toBasis.toMatrix basis.toBasis", "P together with P in Matrix.unitaryGroup n Complex.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:P"),
    ("L-MATRIX-EIGEN-RELATION", "core_lemma", "critical", "Convert the pointwise eigenvector equations to A*P=P*diagonal(ev).", "A * P = P * Matrix.diagonal ev", "The matrix eigen-relation used by final conjugation.", "required", "required", f"atlas-blob:{ATLAS_BLOB}:normal_complex_unitarily_diagonalizable:h1"),
    ("T-CONJUGATED-DIAGONAL", "terminal", "critical", "Compose unitarity and the matrix eigen-relation to prove star(P)*A*P=diagonal(ev).", "SpectralTheorem.normal_complex_unitarily_diagonalizable", "The exact audited conjugated-diagonal anchor.", "required", "required", f"atlas:{ATLAS_REVISION}:SpectralTheorem.normal_complex_unitarily_diagonalizable"),
    ("T-ROOT-COMPOSE", "terminal", "critical", "Convert the explicit unitary membership and conjugated-diagonal equation into the exact frozen root orientation.", "Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor", "Stage1Instances.THM_M_0043.SpectralTheoremTarget.", "required", "required", "local:Stage1_Instances/THM-M-0043/ObligationTree.lean#root_of_exactConjugatedDiagonalAnchor"),
    ("X-SOURCE", "source_boundary", "critical", "Map every material premise and transition to pinpoint primary sources, assumptions, translations, and errata.", "planned primary-source node crosswalk", "Human-source evidence without machine proof credit.", "not_applicable", "required", None),
    ("X-PROVENANCE", "certificate", "critical", "Resolve source blobs, terminal bodies, transitive declarations, pins, licenses, and replay identity.", "planned transitive provenance closure", "Release provenance without proof credit.", "informational", "not_applicable", None),
    ("X-EVIDENCE", "certificate", "high", "Bind node claims to immutable Lean output and structured validation receipts.", "planned content-addressed evidence map", "Evidence references without mathematical proof credit.", "informational", "not_applicable", None),
    ("X-TRUST", "certificate", "critical", "Close root-reachable axioms, unsafe/oracle boundaries, kernel, compiler, and dependency trust.", "planned transitive trust graph", "Trust acceptance without mathematical proof credit.", "informational", "not_applicable", None),
    ("X-READABLE", "documentation", "high", "Provide and independently review a complete readable reconstruction of the joint-eigenspace route.", "planned node-specific readable reconstruction", "Readable coverage and reviewer decision without proof credit.", "not_applicable", "required", None),
    ("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent-verification acceptance.", "planned Stage1 workflow receipts", "Workflow acceptance without mathematical proof credit.", "informational", "not_applicable", None),
)


CHECKED_INTERFACES = {oid("S-INTERFACE"), oid("S-ENCODINGS"), oid("T-ROOT-COMPOSE")}
EXTERNAL_ROUTE = {oid(short) for short, *_ in ROWS if short.startswith(("N-", "B-", "C-", "L-", "T-"))} - {oid("T-ROOT-COMPOSE")}
SOURCE_NA = {oid("S-INTERFACE"), oid("S-ENCODINGS"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"), oid("X-WORKFLOW")}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations: list[dict] = []
    nodes: list[dict] = []

    exclusion_reasons = {
        oid("S-INTERFACE"): "formal_interface_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-ENCODINGS"): "formal_encoding_transport_source_coverage_inherited_from_root_pending_reviewer_acceptance",
        oid("S-FOUNDATION"): "formal_trust_boundary_not_a_human_mathematical_claim_pending_reviewer_acceptance",
        oid("X-SOURCE"): "human_source_boundary_only_pending_independent_source_review",
        oid("X-PROVENANCE"): "provenance_overlay_no_proof_credit_pending_integration_review",
        oid("X-EVIDENCE"): "evidence_overlay_no_proof_credit_pending_integration_review",
        oid("X-TRUST"): "trust_overlay_no_proof_credit_pending_integration_review",
        oid("X-READABLE"): "readability_boundary_only_pending_independent_review",
        oid("X-WORKFLOW"): "workflow_overlay_no_proof_credit_pending_integration_review",
    }

    for short, kind, risk, claim, target, output, machine, human_source, body in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-INTERFACE")}
            else "planned:v1:sha256:" + digest([identifier, kind, claim, target, output])
        )
        excluded = machine != "required" or human_source != "required"
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"), oid("X-WORKFLOW")},
            "machine_eligibility": machine,
            "human_source_eligibility": human_source,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusion_reasons.get(identifier) if excluded else None,
            "terminal_proof_body_id": body,
        })

        if identifier in CHECKED_INTERFACES:
            machine_debt = "M0-L"
        elif identifier == oid("ROOT"):
            machine_debt = "M3"
        elif identifier in EXTERNAL_ROUTE:
            machine_debt = "M1"
        else:
            machine_debt = "M4"
        if identifier == oid("T-CONJUGATED-DIAGONAL"):
            provenance = "anchor-audit:M0043-C01-ATLAS-EXACT"
            evidence = ["worker-anchor-audit:S56-M-0043-ANCHOR-AUDIT-WORKER-20260713"]
        elif identifier == oid("T-ROOT-COMPOSE"):
            provenance = "local-conditional-composition"
            evidence = []
        elif identifier in EXTERNAL_ROUTE:
            provenance = "pinned-visible-atlas-mathlib-route"
            evidence = []
        else:
            provenance = "none"
            evidence = []
        owned_sources = []
        if identifier == oid("T-ROOT-COMPOSE"):
            owned_sources = ["Stage1_Instances/THM-M-0043/ObligationTree.lean"]
        elif identifier == oid("S-ENCODINGS"):
            owned_sources = ["Stage1_Instances/THM-M-0043/Statement.lean"]
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
            "evidence_ids": evidence,
            "source_crosswalk_id": "not-applicable-pending-review" if identifier in SOURCE_NA else "primary-source-node-map-pending",
            "provenance_id": provenance,
            "foundation_profile": "lean4-dependent-type-theory; accepted axiom policy and transitive review pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386+atlas-34ffed3; integration and independent replay pending",
            "computation_record": "none; no native computation, solver, oracle, experiment, or unchecked certificate is credited",
            "step_budget": 80 if risk == "critical" else 40,
            "semantic_step_ledger": {
                "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                "inference": claim,
                "output": output,
                "outgoing_use": "Only the declared proof parent or a typed non-proof support edge may consume this output.",
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0043/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture, audited external route, or checked conditional interface only; no accepted root proof.",
            "task_ids": [ITEM, "S56-M-0043-PROOF"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0043 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "typed-graphs.json", "toolchain and dependency pins"],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{field: row[field] for field in fields} for row in obligations]
    denominator = digest(projection)
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0043-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T09:00:00+08:00",
        "freeze_basis": "Exact statement plus the visible semantic architecture of the immutable Atlas body and its pinned mathlib bridges. Eligibility and denominators are derived without candidate closure status.",
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
            "induction_and_descent": {"status": "not_applicable_pending_independent_approval", "reason": "The finite-dimensional route is a direct construction and has no induction, recursion, minimal-counterexample, or descent branch."},
            "computation": {"status": "not_applicable_pending_independent_approval", "reason": "No reflection, solver, numerical approximation, native code, oracle, experiment, or certificate participates in the visible route."},
            "additional_case_splits": {"status": "not_applicable_pending_independent_approval", "reason": "The route is uniform for every nonempty finite index type; excluded empty dimension and included degenerate matrices are retained in M0043-S-BOUNDARY."},
        },
        "proof_body_aliases": {
            "Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor": "conditional_adapter_no_external_body_credit",
            "Stage1Instances.THM_M_0043.spectralTheoremTarget_iff_conjugatedDiagonalTarget": "statement_transport_no_external_body_credit",
            "Atlas.SpectralTheorem.spectral_theorem.first_conjunct": "deduplicated_to:SpectralTheorem.normal_complex_unitarily_diagonalizable",
        },
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility/risk change, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "audited_candidate_obligation": oid("T-CONJUGATED-DIAGONAL"),
            "audited_candidate_classification": "M1_external_candidate_pending_license_integration_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact external body is not installed or accepted; H0, R0, validation, release, and theorem completion remain open.",
    }

    def edge(edge_id: str, source: str, edge_type: str, target: str, reciprocal: str | None = None) -> dict:
        value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
        if reciprocal is not None:
            value["reciprocal_edge_id"] = reciprocal
        return value

    requires = {
        oid("ROOT"): [oid("T-ROOT-COMPOSE")],
        oid("T-ROOT-COMPOSE"): [oid("T-CONJUGATED-DIAGONAL")],
        oid("T-CONJUGATED-DIAGONAL"): [oid("L-MATRIX-EIGEN-RELATION"), oid("C-UNITARY-MATRIX")],
        oid("L-MATRIX-EIGEN-RELATION"): [oid("L-BASIS-EIGENVECTORS"), oid("C-UNITARY-MATRIX"), oid("C-EIGENVALUES")],
        oid("L-BASIS-EIGENVECTORS"): [oid("T-OPERATOR-DECOMP"), oid("C-BASIS-REINDEX"), oid("C-EIGENVALUES"), oid("C-JOINT-EIGENSPACE")],
        oid("T-OPERATOR-DECOMP"): [oid("T-M-RECONSTRUCT"), oid("C-HERMITIAN-PARTS")],
        oid("T-M-RECONSTRUCT"): [oid("C-HERMITIAN-PARTS")],
        oid("C-UNITARY-MATRIX"): [oid("C-BASIS-REINDEX"), oid("L-UNITARY-BASIS")],
        oid("C-BASIS-REINDEX"): [oid("L-SUBORDINATE-BASIS")],
        oid("L-SUBORDINATE-BASIS"): [oid("B-NONZERO-SUBTYPE"), oid("L-JOINT-ORTHOGONAL")],
        oid("B-NONZERO-SUBTYPE"): [oid("L-JOINT-DECOMP"), oid("L-FINITE-EIGENVALUES"), oid("C-JOINT-EIGENSPACE")],
        oid("L-JOINT-DECOMP"): [oid("L-H-HERMITIAN"), oid("L-K-HERMITIAN"), oid("T-LINEAR-COMMUTE")],
        oid("L-JOINT-ORTHOGONAL"): [oid("L-H-HERMITIAN"), oid("L-K-HERMITIAN"), oid("C-JOINT-EIGENSPACE")],
        oid("T-LINEAR-COMMUTE"): [oid("L-HK-COMMUTE")],
        oid("L-HK-COMMUTE"): [oid("N-NORMAL-COMMUTE"), oid("C-HERMITIAN-PARTS")],
        oid("L-H-HERMITIAN"): [oid("C-HERMITIAN-PARTS")],
        oid("L-K-HERMITIAN"): [oid("C-HERMITIAN-PARTS")],
        oid("C-EIGENVALUES"): [oid("C-JOINT-EIGENSPACE"), oid("C-BASIS-REINDEX")],
    }
    proof: list[dict] = []
    for parent, children in requires.items():
        for child in children:
            req = f"REQ-{parent}-{child}"
            comp = f"CMP-{child}-{parent}"
            proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

    graph_edges = {
        "proof": proof,
        "refinement": [
            edge("REF-ROOT-INTERFACE", oid("ROOT"), "logical_decomposition", oid("S-INTERFACE")),
            edge("REF-ROOT-BOUNDARY", oid("ROOT"), "logical_decomposition", oid("S-BOUNDARY")),
            edge("REF-ROOT-ENCODINGS", oid("ROOT"), "transports", oid("S-ENCODINGS")),
        ],
        "provenance": [
            edge("SRC-ROOT", oid("X-SOURCE"), "source_map", oid("ROOT")),
            edge("SRC-HERMITIAN", oid("X-SOURCE"), "source_map", oid("C-HERMITIAN-PARTS")),
            edge("SRC-JOINT", oid("X-SOURCE"), "source_map", oid("L-JOINT-DECOMP")),
            edge("PROV-ATLAS", oid("X-PROVENANCE"), "provenance_of", oid("T-CONJUGATED-DIAGONAL")),
            edge("PROV-JOINT", oid("X-PROVENANCE"), "provenance_of", oid("L-JOINT-DECOMP")),
            edge("PROV-BASIS", oid("X-PROVENANCE"), "provenance_of", oid("L-SUBORDINATE-BASIS")),
        ],
        "evidence": [
            edge("EVID-ROOT", oid("X-EVIDENCE"), "evidence_for", oid("ROOT")),
            edge("EVID-ATLAS", oid("X-EVIDENCE"), "evidence_for", oid("T-CONJUGATED-DIAGONAL")),
            edge("EVID-COMPOSE", oid("X-EVIDENCE"), "evidence_for", oid("T-ROOT-COMPOSE")),
        ],
        "trust": [
            edge("TRUST-ROOT-FOUNDATION", oid("ROOT"), "trusts", oid("S-FOUNDATION")),
            edge("TRUST-ROOT-CLOSURE", oid("ROOT"), "trusts", oid("X-TRUST")),
            edge("TRUST-CLOSURE-PROV", oid("X-TRUST"), "trusts", oid("X-PROVENANCE")),
        ],
        "documentation": [
            edge("DOC-READABLE-ROOT", oid("X-READABLE"), "documents", oid("ROOT")),
            edge("DOC-READABLE-HERMITIAN", oid("X-READABLE"), "expository_decomposition", oid("C-HERMITIAN-PARTS")),
            edge("DOC-READABLE-JOINT", oid("X-READABLE"), "expository_decomposition", oid("L-JOINT-DECOMP")),
            edge("DOC-READABLE-BASIS", oid("X-READABLE"), "expository_decomposition", oid("C-UNITARY-MATRIX")),
            edge("DOC-SOURCE-ROOT", oid("X-SOURCE"), "documents", oid("ROOT")),
        ],
        "workflow": [
            edge("FLOW-ROOT-PROOF", oid("ROOT"), "workflow_depends_on", oid("T-CONJUGATED-DIAGONAL")),
            edge("FLOW-WORKFLOW-PROV", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-PROVENANCE")),
            edge("FLOW-WORKFLOW-EVID", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-EVIDENCE")),
            edge("FLOW-WORKFLOW-TRUST", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-TRUST")),
            edge("FLOW-WORKFLOW-READABLE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-READABLE")),
            edge("FLOW-WORKFLOW-SOURCE", oid("X-WORKFLOW"), "workflow_depends_on", oid("X-SOURCE")),
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

    proof_reachable = [row["obligation_id"] for row in obligations if row["obligation_id"] in ({oid("ROOT")} | {item for pair in requires.items() for item in (pair[0], *pair[1])})]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0043-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "proof_requires is parent-to-child; reciprocal composes is child-to-parent",
        "nodes": nodes,
        "graphs": graphs,
        "metrics_projection": {
            "proof_reachable_ids": proof_reachable,
            "unique_semantic_leaf_ids": [identifier for identifier in proof_reachable if identifier not in requires],
            "distinct_terminal_body_ids": sorted({row["terminal_proof_body_id"] for row in obligations if row["terminal_proof_body_id"]}),
            "accepted_numerator_ids": [],
            "denominator_ids": ids,
            "alias_and_presentation_nodes_receive_credit": False,
        },
        "closure_boundary": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "remaining_root_cut_set": [oid("T-CONJUGATED-DIAGONAL"), oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-EVIDENCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "composition_certificates": ["Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor"],
            "reason": "The exact external route and its license/integration decision remain uninstalled; all accepted numerator sets stay empty pending proof phase and master validation.",
        },
    }

    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
    for identifier in ids:
        recipes["recipes"].append({
            "recipe_id": f"VAL-{identifier}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0043/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 120,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0043 obligation tree"}],
            "covered_obligation_ids": [identifier],
            "covered_declarations": ["Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor"] if identifier == oid("T-ROOT-COMPOSE") else ["SpectralTheorem.normal_complex_unitarily_diagonalizable"] if identifier == oid("T-CONJUGATED-DIAGONAL") else [],
        })
    return registry, bundle, recipes


def main() -> None:
    values = build()
    for name, value in zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), values):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    edge_count = sum(len(graph["edges"]) for graph in values[1]["graphs"].values())
    print(f"wrote {len(ROWS)} obligations and {edge_count} typed edges")
    print(values[0]["denominator_sha256"])


if __name__ == "__main__":
    main()
