#!/usr/bin/env python3
"""Build the frozen THM-M-0044 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0044-OBLIGATION_TREE"
THEOREM = "THM-M-0044"
PREFIX = "M0044-"
ROOT_EXPRESSION = "f9a0f27af3e6287fc303bfbd9ecf382111bd44ed8d60e27cff6d0acc59b1052b"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
)


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# short id, registry kind, graph-node kind, risk, claim, formal target, output,
# machine eligibility, human-source eligibility, terminal body, step budget
ROWS = (
    ("ROOT", "root", "root", "critical",
     "Every finite rectangular real or complex matrix has the frozen full square-factor singular value decomposition.",
     "Stage1Instances.THM_M_0044.SingularValueDecompositionTarget",
     "The exact closed Real-and-Complex canonical proposition.",
     "required", "required", None, 12),
    ("S-INTERFACE", "definition", "definition", "critical",
     "Preserve finite rectangular dimensions, square unitary factors, nonnegative real singular data, explicit rectangular Sigma, and A = U * Sigma * star V.",
     "Stage1Instances.THM_M_0044.{IsRectangularDiagonal,IsFullSVD,FullSVDOver,SingularValueDecompositionTarget}",
     "The exact formal domain, witnesses, invariants, and conclusion.",
     "required", "not_applicable", None, 24),
    ("S-BOUNDARY", "branch", "branch", "high",
     "Close zero-row and zero-column dimensions without positivity, Nonempty, rank, or invertibility assumptions.",
     "Stage1Instances.THM_M_0044.{zeroByNBoundary,mByZeroBoundary}",
     "The checked empty-dimension branches for both selected scalar fields.",
     "required", "required", "repo:Stage1Instances.THM_M_0044.ObligationTree.selectedEmptyDimensions", 30),
    ("S-ENCODING", "transport", "transport", "high",
     "Relate the named root exactly to its direct expansion and only one-way from the stronger open RCLike formulation.",
     "Stage1Instances.THM_M_0044.{singularValueDecompositionTarget_iff_directFullSVDShape,rclikeFullSVDShape_implies_target}",
     "Checked transport directions with no thin, compact, real-only, or square substitution.",
     "required", "not_applicable", "repo:Stage1Instances.THM_M_0044.singularValueDecompositionTarget_iff_directFullSVDShape", 18),
    ("S-FOUNDATION", "terminal", "certificate", "critical",
     "Audit classical choice, square roots, basis extension, extensionality, quotients, axioms, imports, computation policy, and the trusted computing base.",
     "Lean 4.29.0 and pinned mathlib transitive trust closure",
     "An accepted foundation and TCB boundary for every terminal body.",
     "required", "not_applicable", None, 45),
    ("B-REAL-DIMENSIONS", "branch", "branch", "critical",
     "Split the real target exhaustively into m=0, n=0, and m>0 with n>0, then recompose FullSVDOver Real.",
     "planned Nat dimension split and exact Real FullSVDOver recomposition",
     "The real target for all finite dimensions, including the overlapping 0-by-0 boundary.",
     "required", "required", None, 35),
    ("B-COMPLEX-DIMENSIONS", "branch", "branch", "critical",
     "Split the complex target exhaustively into m=0, n=0, and m>0 with n>0, then recompose FullSVDOver Complex.",
     "planned Nat dimension split and exact Complex FullSVDOver recomposition",
     "The complex target for all finite dimensions, including the overlapping 0-by-0 boundary.",
     "required", "required", None, 35),
    ("T-REAL-NONEMPTY", "terminal", "terminal", "critical",
     "Assemble a full SVD witness for every positive-dimensional real rectangular matrix.",
     "planned positive-dimension real IsFullSVD composition",
     "The nonempty branch of FullSVDOver Real.",
     "required", "required", None, 42),
    ("T-COMPLEX-NONEMPTY", "terminal", "terminal", "critical",
     "Assemble a full SVD witness for every positive-dimensional complex rectangular matrix.",
     "planned positive-dimension complex IsFullSVD composition",
     "The nonempty branch of FullSVDOver Complex.",
     "required", "required", None, 42),
    ("N-LINEAR-MAP", "reduction", "reduction", "critical",
     "Transport an arbitrary m-by-n matrix to the matching finite Euclidean linear map and back, preserving adjoint and multiplication orientation.",
     "planned Matrix.toEuclideanLin and adjoint/conjugate-transpose compatibility package",
     "A representation in which the finite-dimensional spectral interfaces apply.",
     "required", "required", None, 65),
    ("C-GRAM", "construction", "construction", "critical",
     "Construct the right Gram operator A* A on the n-dimensional domain, including empty dimensions.",
     "planned Gram matrix/linear-map construction",
     "A square endomorphism whose eigenvectors are candidate right singular vectors.",
     "required", "required", None, 42),
    ("L-GRAM-HERMITIAN", "lemma", "core_lemma", "high",
     "Prove that A* A is Hermitian/self-adjoint and positive semidefinite in the selected representation.",
     "Matrix.isHermitian_conjTranspose_mul_self plus linear-map positivity bridges",
     "Hermitian spectral eligibility and nonnegative eigenvalue data.",
     "required", "required", None, 55),
    ("X-SPECTRAL", "lemma", "bridge", "critical",
     "Apply the pinned symmetric-linear-map eigenvector-basis theorem to A† A and audit the terminal library body rather than treating the invocation as primitive.",
     "LinearMap.IsSymmetric.eigenvectorBasis and LinearMap.IsSymmetric.apply_eigenvectorBasis",
     "A full orthonormal right eigenbasis and diagonal eigenvalue equation.",
     "required", "required", "mathlib@8a178386:LinearMap.IsSymmetric.eigenvectorBasis", 36),
    ("C-RIGHT-EIGENBASIS", "construction", "construction", "critical",
     "Extract and orient a complete right orthonormal eigenbasis from the spectral theorem.",
     "planned basis indexed by Fin n with A* A eigenvector equations",
     "Right singular vectors v_j with a complete orthonormal-basis invariant.",
     "required", "required", None, 60),
    ("C-SINGULAR-VALUES", "construction", "construction", "critical",
     "Use the pinned LinearMap.singularValues sequence and restrict it to the exact Fin (min m n) data after proving the rank and index transports.",
     "LinearMap.singularValues with planned finite-index restriction",
     "Real singular data sigma with squared-value equations.",
     "required", "required", "mathlib@8a178386:LinearMap.singularValues", 72),
    ("L-SINGULAR-NONNEG", "lemma", "core_lemma", "high",
     "Prove sigma_j is nonnegative and its square is the matching Gram eigenvalue.",
     "planned Real.sqrt_nonneg and Gram eigenvalue positivity package",
     "Nonnegativity and normalization equations required by IsFullSVD.",
     "required", "required", None, 48),
    ("L-RANK-BOUNDS", "lemma", "core_lemma", "critical",
     "For r = finrank(range A), prove r <= n and r <= m, hence r <= min(m,n), with exact Euclidean-space cardinal transports.",
     "planned LinearMap.finrank_range bounds and FiniteDimensional.finrank_fin compatibility",
     "The rank inequalities required by positive-prefix, left-extension, and rectangular-tail indices.",
     "required", "required", None, 62),
    ("B-SINGULAR-SPLIT", "branch", "branch", "critical",
     "Split every relevant singular direction into sigma_j > 0 and sigma_j = 0 and prove the split exhaustive.",
     "planned finite exhaustive positivity/zero branch recomposition",
     "A complete partition of right singular directions, including rank-deficient tails.",
     "required", "required", None, 38),
    ("B-POSITIVE", "branch", "branch", "high",
     "Handle directions with positive singular value by normalized application of A.",
     "planned positive-sigma branch",
     "Left-vector data for every positive singular direction.",
     "required", "required", None, 28),
    ("C-POSITIVE-LEFT", "construction", "construction", "critical",
     "For sigma_j > 0 construct u_j = sigma_j^-1 A v_j and prove A v_j = sigma_j u_j.",
     "planned normalized left-singular-vector construction",
     "Positive left singular vectors and their defining intertwining equation.",
     "required", "required", None, 70),
    ("L-POSITIVE-LEFT-ON", "lemma", "core_lemma", "critical",
     "Use the Gram eigenvalue equations to prove the positive left singular vectors are orthonormal.",
     "planned inner-product calculation for normalized images",
     "An orthonormal positive left family.",
     "required", "required", None, 82),
    ("B-ZERO", "branch", "branch", "critical",
     "Handle zero singular directions without dividing by zero and track domain-kernel and codomain-complement dimensions.",
     "planned zero-singular-value branch",
     "A complete rank-deficient and zero-tail construction.",
     "required", "required", None, 35),
    ("L-ZERO-KERNEL", "lemma", "core_lemma", "critical",
     "Show a zero Gram eigenvalue implies A v_j = 0 and characterize the unused left complement needed for a full basis.",
     "planned norm-square/kernel lemma",
     "Zero-column equations plus the exact remaining left dimension.",
     "required", "required", None, 68),
    ("C-LEFT-COMPLETE", "construction", "construction", "critical",
     "Extend the positive left family to a full Fin m orthonormal basis; zero/tail columns need no prescribed left vector, including m=0.",
     "Orthonormal.exists_orthonormalBasis_extension_of_card_eq plus finite cardinal arithmetic",
     "A complete left orthonormal basis with the prescribed singular-vector prefix.",
     "required", "required", None, 85),
    ("L-BASIS-INVARIANTS", "lemma", "core_lemma", "critical",
     "Prove all chosen extensions preserve indexing, orthonormality, positive equations, zero equations, and independence of unused choices.",
     "planned basis-extension invariant package",
     "Two compatible full bases and all columnwise action equations.",
     "required", "required", None, 88),
    ("C-UNITARY", "construction", "construction", "high",
     "Convert the left and right orthonormal bases to square unitary matrices in the orientation used by the frozen equality.",
     "LinearIsometryEquiv.toMatrix_mem_unitaryGroup plus orientation bridges",
     "Square U and V with membership in Matrix.unitaryGroup.",
     "required", "required", None, 62),
    ("N-MIN-INDEX", "reduction", "normalization", "critical",
     "Reindex rank, positive, zero, and tail directions into the exact Fin (min m n) convention without ordering or sign ambiguity.",
     "planned finite-cardinality and permutation normalization",
     "The precise dependent indices used by the frozen rectangular diagonal.",
     "required", "required", None, 76),
    ("N-ORDER-ALIGN", "reduction", "normalization", "critical",
     "Align the right eigenbasis index with sq_singularValues_fin and decreasing singular-value order, preserving each exact Fin n column position.",
     "planned indexed eigenvalue/singularValues/eigenvectorBasis transport",
     "One stable index relation shared by sigma, v_j, the support cutoff, and Sigma.",
     "required", "required", None, 78),
    ("L-ZERO-TAIL", "lemma", "core_lemma", "critical",
     "For every right-basis position at or beyond rank, and every j >= min(m,n) when n>m, prove sigma_j=0 and A v_j=0.",
     "planned singularValues support cutoff plus ker_adjoint_comp_self argument",
     "All zero and rectangular-tail column action equations.",
     "required", "required", None, 82),
    ("C-SIGMA", "construction", "construction", "high",
     "Build the explicit m-by-n rectangular Sigma and prove its off-diagonal entries vanish and diagonal entries are the embedded nonnegative sigma values.",
     "Stage1Instances.THM_M_0044.IsRectangularDiagonal with the frozen dependent if-expression",
     "The exact rectangular diagonal witness required by IsFullSVD.",
     "required", "required", None, 58),
    ("L-ENTRYWISE", "lemma", "core_lemma", "critical",
     "Prove A = U * Sigma * star V entrywise from the full-basis column equations, including all zero and rectangular-tail indices.",
     "planned Matrix.ext and finite-sum orthonormal-basis calculation",
     "The exact multiplication equality in the selected star orientation.",
     "required", "required", None, 100),
    ("T-REAL", "transport", "transport", "high",
     "Recompose the real dimension branches into the exact real half of the canonical root.",
     "Stage1Instances.THM_M_0044.ObligationTree.RealFullSVDPackage",
     "Stage1Instances.THM_M_0044.ObligationTree.RealFullSVDPackage.",
     "required", "required", None, 18),
    ("T-COMPLEX", "transport", "transport", "high",
     "Recompose the complex dimension branches into the exact complex half of the canonical root.",
     "Stage1Instances.THM_M_0044.ObligationTree.ComplexFullSVDPackage",
     "Stage1Instances.THM_M_0044.ObligationTree.ComplexFullSVDPackage.",
     "required", "required", None, 18),
    ("T-ASSEMBLE", "terminal", "terminal", "critical",
     "Consume the exact real and complex packages and form the canonical conjunction.",
     "Stage1Instances.THM_M_0044.ObligationTree.root_of_real_and_complex",
     "The exact frozen SingularValueDecompositionTarget.",
     "required", "required", "repo:Stage1Instances.THM_M_0044.ObligationTree.root_of_real_and_complex", 8),
    ("X-SOURCE", "terminal", "terminal", "critical",
     "Map every material SVD transition to a reviewed primary theorem, definitions, assumptions, empty-dimension reconciliation, orientation, errata, and historical attribution.",
     "Axler 4e Section 7E and primary/historical source packet pending",
     "Human-source coverage without machine proof credit.",
     "not_applicable", "required", None, 90),
    ("X-PROVENANCE", "terminal", "certificate", "critical",
     "Audit wrappers, terminal bodies, aliases, imports, immutable origins, licenses, and revocations without duplicate proof credit.",
     "terminal proof-body provenance packets pending",
     "Body-level provenance coverage without mathematical proof credit.",
     "informational", "not_applicable", None, 55),
    ("X-TRUST", "terminal", "certificate", "critical",
     "Audit Lean, mathlib, axioms, compiled artifacts, unsafe/oracle boundaries, replay, and supply-chain trust transitively.",
     "Lean 4.29.0 and mathlib 8a178386 transitive closure pending",
     "Release-grade trust coverage without mathematical proof credit.",
     "informational", "not_applicable", None, 55),
    ("X-READABLE", "terminal", "terminal", "high",
     "Produce and independently review the complete node-specific mathematical reconstruction.",
     "proof outline and independent reader receipt pending",
     "Readable coverage without machine proof credit.",
     "not_applicable", "required", None, 90),
    ("X-WORKFLOW", "terminal", "terminal", "critical",
     "Bind proof, composition, source, readability, validation, freshness, revocation, independent verification, and release tasks.",
     "Stage1 task and receipt closure pending",
     "Workflow acceptance without mathematical proof credit.",
     "informational", "not_applicable", None, 40),
)


CHECKED_LOCAL = {
    oid("S-BOUNDARY"), oid("S-ENCODING"), oid("T-ASSEMBLE")
}


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(ids: list[str], edges: list[dict]) -> dict:
    outgoing = {identifier: [] for identifier in ids}
    incoming = {identifier: [] for identifier in ids}
    for value in edges:
        outgoing[value["from"]].append(value["edge_id"])
        incoming[value["to"]].append(value["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    nodes = []
    for short, reg_kind, node_kind, risk, claim, target, output, machine, human, body, budget in ROWS:
        identifier = oid(short)
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if short in {"ROOT", "S-INTERFACE"}
            else "planned:v1:sha256:" + digest([identifier, reg_kind, claim, target, output])
        )
        reasons = []
        if machine != "required":
            reasons.append("no_machine_proof_credit")
        if human != "required":
            reasons.append("not_a_distinct_human_mathematical_claim")
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": reg_kind,
            "root_relevant": True,
            "machine_eligibility": machine,
            "human_source_eligibility": human,
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": (
                "_and_".join(reasons) + "_pending_independent_approval" if reasons else None
            ),
            "terminal_proof_body_id": body,
        })
        if short == "ROOT":
            machine_debt = "M3"
        elif identifier in CHECKED_LOCAL or short in {"S-INTERFACE", "L-GRAM-HERMITIAN", "X-SPECTRAL",
                       "C-LEFT-COMPLETE", "C-UNITARY"}:
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        owned_sources = []
        if identifier in {oid("T-REAL"), oid("T-COMPLEX"), oid("T-ASSEMBLE")}:
            owned_sources = ["Stage1_Instances/THM-M-0044/ObligationTree.lean"]
        elif identifier in {oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-ENCODING")}:
            owned_sources = ["Stage1_Instances/THM-M-0044/Statement.lean"]
        nodes.append({
            "node_id": f"{THEOREM}-{short}",
            "obligation_id": identifier,
            "kind": node_kind,
            "human_statement": claim,
            "formal_target": target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": machine_debt,
            "readability_debt": "R3",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if human != "required"
                else "Axler-4e-7E-node-map-pending-independent-review"
            ),
            "provenance_id": (
                "repo-local-checked-interface" if identifier in CHECKED_LOCAL
                else "anchor-audit:M0044-C01-MATHLIB-SVD-SUBSTRATE"
                if short in {"L-GRAM-HERMITIAN", "X-SPECTRAL", "C-LEFT-COMPLETE", "C-UNITARY"}
                else "support-boundary-pending" if short.startswith("X-") else "none"
            ),
            "foundation_profile": "lean4-dependent-type-theory+classical-finite-linear-algebra; accepted transitive axiom policy pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure and independent replay pending",
            "computation_record": "none; no numerical SVD, oracle, solver, native shortcut, experiment, or unchecked certificate is credited",
            "step_budget": budget,
            "semantic_step_ledger": {
                "premises": "The exact formal context and only conclusions named by incoming proof_requires edges.",
                "inference": target,
                "output": output,
                "outgoing_use": "Only a declared proof parent or typed non-proof support edge may consume this output.",
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0044/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or conditional interface only; no accepted root proof, H0, R0, audit completion, or theorem completion.",
            "task_ids": [ITEM, "S56-M-0044-PROOF", "S56-M-0044-VALIDATION"],
            "owned_sources": owned_sources,
            "owner": "THM-M-0044 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_LOCAL else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "source crosswalk", "toolchain", "dependency pin",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_LOCAL else "open",
            },
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{key: row[key] for key in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0044-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "Exact elaborated full rectangular Real-and-Complex target plus the bounded immutable anchor audit; spectral/Gram and basis-completion architecture selected before proof closure observation.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
            "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")],
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility, risk, or weight change requires a new registry version and append-only old/new ID delta.",
        "append_only_delta": [],
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(CHECKED_LOCAL),
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "mandatory_layer_analysis": {
            "S": [oid("S-INTERFACE"), oid("S-BOUNDARY"), oid("S-ENCODING"), oid("S-FOUNDATION")],
            "N": [oid("N-LINEAR-MAP"), oid("N-MIN-INDEX"), oid("N-ORDER-ALIGN")],
            "B": [oid("B-REAL-DIMENSIONS"), oid("B-COMPLEX-DIMENSIONS"), oid("B-SINGULAR-SPLIT"), oid("B-POSITIVE"), oid("B-ZERO")],
            "C": [row["obligation_id"] for row in obligations if row["kind"] == "construction"],
            "L": [row["obligation_id"] for row in obligations if row["kind"] == "lemma"],
            "X": [oid("X-SPECTRAL"), oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "T": [oid("T-REAL-NONEMPTY"), oid("T-COMPLEX-NONEMPTY"), oid("T-REAL"), oid("T-COMPLEX"), oid("T-ASSEMBLE"), oid("ROOT")],
            "not_applicable_layers": [],
        },
        "obligations": obligations,
        "status_boundary": "Frozen semantic inventory and eligibility only; no SVD proof, accepted source/readability/trust closure, audit completion, or theorem completion.",
    }

    requirements = {
        oid("ROOT"): [oid("T-ASSEMBLE")],
        oid("T-ASSEMBLE"): [oid("T-REAL"), oid("T-COMPLEX")],
        oid("T-REAL"): [oid("B-REAL-DIMENSIONS")],
        oid("T-COMPLEX"): [oid("B-COMPLEX-DIMENSIONS")],
        oid("B-REAL-DIMENSIONS"): [oid("S-BOUNDARY"), oid("T-REAL-NONEMPTY")],
        oid("B-COMPLEX-DIMENSIONS"): [oid("S-BOUNDARY"), oid("T-COMPLEX-NONEMPTY")],
        oid("T-REAL-NONEMPTY"): [
            oid("C-UNITARY"), oid("L-SINGULAR-NONNEG"), oid("C-SIGMA"), oid("L-ENTRYWISE")
        ],
        oid("T-COMPLEX-NONEMPTY"): [
            oid("C-UNITARY"), oid("L-SINGULAR-NONNEG"), oid("C-SIGMA"), oid("L-ENTRYWISE")
        ],
        oid("C-GRAM"): [oid("N-LINEAR-MAP")],
        oid("L-GRAM-HERMITIAN"): [oid("C-GRAM")],
        oid("X-SPECTRAL"): [oid("C-GRAM"), oid("L-GRAM-HERMITIAN")],
        oid("C-RIGHT-EIGENBASIS"): [oid("X-SPECTRAL")],
        oid("C-SINGULAR-VALUES"): [oid("C-GRAM"), oid("C-RIGHT-EIGENBASIS")],
        oid("L-SINGULAR-NONNEG"): [oid("C-SINGULAR-VALUES"), oid("L-GRAM-HERMITIAN")],
        oid("L-RANK-BOUNDS"): [oid("N-LINEAR-MAP")],
        oid("N-ORDER-ALIGN"): [
            oid("C-RIGHT-EIGENBASIS"), oid("C-SINGULAR-VALUES"), oid("L-RANK-BOUNDS")
        ],
        oid("B-SINGULAR-SPLIT"): [
            oid("L-SINGULAR-NONNEG"), oid("L-RANK-BOUNDS"), oid("N-ORDER-ALIGN"),
            oid("B-POSITIVE"), oid("B-ZERO"),
        ],
        oid("B-POSITIVE"): [oid("C-POSITIVE-LEFT"), oid("L-POSITIVE-LEFT-ON")],
        oid("C-POSITIVE-LEFT"): [oid("C-RIGHT-EIGENBASIS"), oid("C-SINGULAR-VALUES")],
        oid("L-POSITIVE-LEFT-ON"): [
            oid("C-POSITIVE-LEFT"), oid("L-GRAM-HERMITIAN"), oid("N-ORDER-ALIGN")
        ],
        oid("B-ZERO"): [oid("L-ZERO-KERNEL")],
        oid("L-ZERO-KERNEL"): [
            oid("C-GRAM"), oid("C-RIGHT-EIGENBASIS"), oid("C-SINGULAR-VALUES")
        ],
        oid("L-ZERO-TAIL"): [
            oid("L-ZERO-KERNEL"), oid("L-RANK-BOUNDS"), oid("N-ORDER-ALIGN")
        ],
        oid("C-LEFT-COMPLETE"): [oid("L-POSITIVE-LEFT-ON"), oid("L-RANK-BOUNDS")],
        oid("L-BASIS-INVARIANTS"): [
            oid("B-SINGULAR-SPLIT"), oid("C-RIGHT-EIGENBASIS"),
            oid("C-LEFT-COMPLETE"), oid("L-ZERO-TAIL"),
        ],
        oid("C-UNITARY"): [
            oid("C-RIGHT-EIGENBASIS"), oid("C-LEFT-COMPLETE"), oid("L-BASIS-INVARIANTS")
        ],
        oid("N-MIN-INDEX"): [oid("L-RANK-BOUNDS"), oid("N-ORDER-ALIGN")],
        oid("C-SIGMA"): [oid("C-SINGULAR-VALUES"), oid("N-MIN-INDEX")],
        oid("L-ENTRYWISE"): [
            oid("C-UNITARY"), oid("C-SIGMA"), oid("L-ZERO-TAIL"),
            oid("L-BASIS-INVARIANTS"),
        ],
    }
    proof_parents: dict[str, list[str]] = {identifier: [] for identifier in ids}
    for parent, children in requirements.items():
        for child in children:
            proof_parents[child].append(parent)
    node_by_id = {node["obligation_id"]: node for node in nodes}
    for identifier, node in node_by_id.items():
        children = requirements.get(identifier, [])
        parents = proof_parents[identifier]
        node["semantic_step_ledger"] = {
            "premises": children if children else ["exact-formal-context-no-hidden-proof-premise"],
            "inference": node["formal_target"],
            "output": node["output"],
            "outgoing_use": parents if parents else ["typed-non-proof-edge-or-canonical-root-boundary"],
        }
    proof_edges = []
    sequence = 0
    for parent, children in requirements.items():
        for child in children:
            sequence += 1
            req = f"P{sequence:02d}-REQ"
            comp = f"P{sequence:02d}-COMP"
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, comp),
                edge(comp, child, "composes", parent, req),
            ])

    def edges(prefix: str, edge_type: str, pairs: list[tuple[str, str]]) -> list[dict]:
        return [edge(f"{prefix}{index:02d}", source, edge_type, target)
                for index, (source, target) in enumerate(pairs, 1)]

    graph_edges = {
        "proof": proof_edges,
        "refinement": edges("R", "logical_decomposition", [
            (oid("ROOT"), oid("S-INTERFACE")), (oid("ROOT"), oid("S-BOUNDARY")),
            (oid("ROOT"), oid("S-ENCODING")), (oid("ROOT"), oid("S-FOUNDATION")),
            (oid("C-GRAM"), oid("L-GRAM-HERMITIAN")),
            (oid("C-SINGULAR-VALUES"), oid("L-SINGULAR-NONNEG")),
            (oid("C-LEFT-COMPLETE"), oid("L-BASIS-INVARIANTS")),
        ]),
        "provenance": edges("V", "provenance_of", [
            (oid("X-PROVENANCE"), oid("ROOT")), (oid("X-PROVENANCE"), oid("X-SPECTRAL")),
            (oid("X-PROVENANCE"), oid("T-ASSEMBLE")),
        ]) + edges("S", "source_map", [
            (identifier, oid("X-SOURCE")) for identifier in ids
            if identifier not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
        ]),
        "evidence": [],
        "trust": edges("T", "trusts", [
            (oid("ROOT"), oid("S-FOUNDATION")), (oid("ROOT"), oid("X-TRUST")),
            (oid("X-SPECTRAL"), oid("X-TRUST")), (oid("T-ASSEMBLE"), oid("X-TRUST")),
        ]),
        "documentation": edges("D", "documents", [
            (oid("X-READABLE"), oid("ROOT")), (oid("X-SOURCE"), oid("T-REAL")),
            (oid("X-SOURCE"), oid("T-COMPLEX")),
            (oid("X-SOURCE"), oid("L-ENTRYWISE")),
        ]),
        "workflow": edges("W", "workflow_depends_on", [
            (oid("ROOT"), oid("X-SOURCE")), (oid("ROOT"), oid("X-PROVENANCE")),
            (oid("ROOT"), oid("X-TRUST")), (oid("ROOT"), oid("X-READABLE")),
            (oid("ROOT"), oid("X-WORKFLOW")), (oid("X-WORKFLOW"), oid("T-ASSEMBLE")),
        ]),
    }
    graphs = {name: graph(ids, graph_edges[name]) for name in GRAPH_NAMES}
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": "THM-M-0044-OBLIGATIONS-v1",
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id",
        "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent. Other graphs use their named edge semantics and never supply proof credit.",
        "nodes": nodes,
        "graphs": graphs,
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(CHECKED_LOCAL),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "composition_certificates": [
                "Stage1Instances.THM_M_0044.ObligationTree.root_of_real_and_complex",
            ],
            "remaining_root_cut_set": [
                oid("T-REAL"), oid("T-COMPLEX"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "The exact real and complex packages and every substantive positive-dimension construction beneath them remain open; checked conjunction composition does not prove either premise.",
        },
    }

    recipes = []
    for node in nodes:
        covered = []
        if node["obligation_id"] == oid("ROOT"):
            covered = ["Stage1Instances.THM_M_0044.SingularValueDecompositionTarget"]
        elif node["obligation_id"] in CHECKED_LOCAL:
            covered = [node["formal_target"]]
        recipes.append({
            "recipe_id": node["validation_spec_id"],
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0044/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 60,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "exact PASS prefix plus recomputed denominator"}],
            "covered_obligation_ids": [node["obligation_id"]],
            "covered_declarations": covered,
        })
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "recipes": recipes,
        "status_boundary": "These worker recipes validate the frozen architecture and checked conditional interfaces, not the open mathematical packages or release gates.",
    }
    return registry, bundle, specs


def main() -> None:
    registry, bundle, specs = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", specs),
    ):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(registry["denominator_sha256"])


if __name__ == "__main__":
    main()
