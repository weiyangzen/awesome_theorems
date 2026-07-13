#!/usr/bin/env python3
"""Build the frozen THM-M-0045 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0045-OBLIGATION_TREE"
THEOREM = "THM-M-0045"
PREFIX = "M0045-"
EXTERNAL_REVISION = "0a539f0ce764fd16726509b62ed7b870461070eb"
EXTERNAL_SOURCE_SHA256 = "8fc4d47249d8bcc75c02fedc6d9b0008f7c0127c501f608d4226a7f5872f4bc3"


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def spec(
    oid: str,
    kind: str,
    risk: str,
    statement: str,
    formal_target: str,
    output: str,
    source: str,
    budget: int,
) -> dict:
    return {
        "id": oid,
        "kind": kind,
        "risk": risk,
        "statement": statement,
        "formal_target": formal_target,
        "output": output,
        "source": source,
        "budget": budget,
    }


# The inventory follows the mathematical architecture visible in the immutable
# 300-line external source. Status is deliberately assigned only after this list.
SPECS = [
    spec("M0045-ROOT", "root", "critical", "Every finite complex square matrix is unitarily similar to an upper triangular matrix in the exact frozen convention.", "Stage1Instances.THM_M_0045.SchurTriangularizationTarget", "The exact canonical proposition.", "Statement.lean; expression sha256 275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b", 12),
    spec("M0045-S-TARGET", "definition", "critical", "Freeze the ordered n, A, U binders, complex scalar field, unitary predicate, conjugation orientation, and BlockTriangular id conclusion.", "checked target-interface audit of Stage1Instances.THM_M_0045.SchurTriangularizationTarget", "A binder, domain, and conclusion identity certificate for the root, not a second proof of it.", "Statement.lean:16-21; statement.json", 24),
    spec("M0045-S-DOMAIN", "normalization", "high", "Specialize Schur triangularization to Matrix (Fin n) (Fin n) Complex with its canonical finite linear order and decidable equality.", "forall n : Nat, Matrix (Fin n) (Fin n) Complex", "The root's exact domain and typeclass context.", "Statement.lean:17-21", 16),
    spec("M0045-S-BOUNDARY", "branch", "high", "Retain n = 0 and n = 1, and impose no invertibility, normality, diagonalizability, or nonzero-dimension hypothesis.", "Stage1Instances.THM_M_0045.ObligationTree.DimensionBoundary", "Every natural dimension is zero or positive, with zero and one still inside the universal target.", "BoundaryProbe.lean:14-31; ObligationTree.lean:DimensionBoundary", 18),
    spec("M0045-S-EQUATION", "transport", "critical", "Transport one unitary factorization A = U*T*star U with upper-triangular T to the target conjugation convention.", "Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt", "Matrix.BlockTriangular (star U * A * U) id for the same witness U.", "ObligationTree.lean:equationWitness_implies_targetAt", 20),
    spec("M0045-S-FOUNDATION", "certificate", "critical", "Account for Lean, mathlib, propext, Classical.choice, Quot.sound, exact imports, and the no-oracle/no-numerical-computation policy.", "#print axioms root_of_equationPackage and equationWitness_implies_targetAt", "A versioned foundation and TCB boundary.", "ObligationTree.lean axiom probes; anchor-audit.json immutable_environment", 24),
    spec("M0045-N-MATRIX-OPERATOR", "transport", "critical", "Transport A to its Euclidean-space linear endomorphism and its matrix back in an orthonormal basis.", "Matrix.toEuclideanLin and LinearMap.toMatrixOrthonormal", "A matrix representation of the same endomorphism.", "external SchurTriangulation.lean:252-259,288-295", 36),
    spec("M0045-N-REINDEX", "transport", "high", "Construct the Boolean-sigma/Fin(m+n) index bridge used by the recursive basis, then reindex the resulting Fin d basis to the original finite linearly ordered matrix index type.", "Fin.subNat'; Equiv.finAddEquivSigmaCond; Fintype.orderIsoFinOfCardEq; OrthonormalBasis.reindex", "An orthonormal basis indexed first by Fin(m+n) and finally by the original matrix index type, with order cases preserved.", "external SchurTriangulation.lean:29-70,171-172,248-265", 70),
    spec("M0045-B-DIMENSION", "branch", "critical", "Split the recursive inner-product space into the nontrivial and subsingleton cases and recombine exhaustively.", "if hE : Nontrivial E then ... else ...", "A SchurTriangulationAux package in either dimension case.", "external SchurTriangulation.lean:150-154,223-230", 18),
    spec("M0045-B-ZERO", "branch", "high", "For a subsingleton space, use dimension zero, the empty orthonormal basis, and vacuous upper triangularity.", "Module.finrank_zero_of_subsingleton; Basis.empty; nofun", "The zero-dimensional auxiliary package.", "external SchurTriangulation.lean:223-230", 20),
    spec("M0045-B-NONTRIVIAL", "branch", "critical", "For a nontrivial space, choose an eigenvalue, split off its eigenspace, recursively triangularize the orthogonal complement, and assemble the invariant basis.", "nontrivial branch of LinearMap.SchurTriangulationAux.of", "The positive-dimensional auxiliary package.", "external SchurTriangulation.lean:154-222", 24),
    spec("M0045-C-EIGENVALUE", "construction", "critical", "Choose an eigenvalue of the endomorphism over an algebraically closed RCLike field.", "let mu : f.Eigenvalues := default", "An eigenvalue with a nonzero eigenvector witness.", "external SchurTriangulation.lean:155; Module.End.exists_eigenvalue", 28),
    spec("M0045-C-EIGENSPACE", "construction", "critical", "Construct the selected eigenspace V and retain its nontriviality for the descent measure.", "let V : Submodule K E := f.eigenspace mu", "A nonzero invariant submodule V.", "external SchurTriangulation.lean:156,200-202,236", 32),
    spec("M0045-C-ORTHOGONAL", "construction", "critical", "Construct W = V orthogonal and record the V/W orthogonal-family facts.", "let W : Submodule K E := V orthogonal", "The orthogonal complement W and orthogonality between V and W.", "external SchurTriangulation.lean:157,164", 28),
    spec("M0045-C-COMPRESSED", "construction", "critical", "Restrict f to W and project back to W to obtain the smaller compressed endomorphism g.", "orthogonalProjection W comp f.domRestrict W", "An endomorphism g of W for the recursive call.", "external SchurTriangulation.lean:160", 26),
    spec("M0045-C-RECURSION", "construction", "critical", "Recursively construct an orthonormal upper-triangular basis for the compressed endomorphism on W.", "LinearMap.SchurTriangulationAux.of g", "Dimension n, basis bW, and triangularity hg for g.", "external SchurTriangulation.lean:161", 30),
    spec("M0045-L-DESCENT", "core_lemma", "critical", "Prove finrank W < finrank E using positivity of finrank V and finrank additivity.", "Module.finrank K W < Module.finrank K E", "The well-founded recursion decrease.", "external SchurTriangulation.lean:231-237", 34),
    spec("M0045-C-EIGENBASIS", "construction", "high", "Choose the standard orthonormal basis bV of the eigenspace V.", "stdOrthonormalBasis K V", "An orthonormal basis bV indexed by Fin (finrank K V).", "external SchurTriangulation.lean:163", 18),
    spec("M0045-C-COMPLEMENT-BASIS", "construction", "high", "Use the recursively returned orthonormal basis bW of W with its upper-triangular compressed matrix invariant.", "recursive fields bW and hg", "An orthonormal basis of W carrying the recursive invariant.", "external SchurTriangulation.lean:161,168", 18),
    spec("M0045-C-INTERNAL-SUM", "construction", "critical", "Prove the V/W orthogonal family is internal and spans top.", "DirectSum.IsInternal (cond . V W)", "The internal direct-sum certificate needed to collect the bases.", "external SchurTriangulation.lean:164-170", 38),
    spec("M0045-C-COLLECTED-BASIS", "construction", "critical", "Collect bV and bW into an orthonormal basis of E and reindex the Boolean sigma index to Fin (m+n).", "int.collectedOrthonormalBasis hV B; Equiv.finAddEquivSigmaCond", "The assembled orthonormal basis of E.", "external SchurTriangulation.lean:168-176", 52),
    spec("M0045-B-ENTRY-SPLIT", "branch", "critical", "For every entry strictly below the diagonal, split whether the column and row lie in the V block or W block, including the impossible cross-index case.", "if hj : j < m then if hi : i < m then ... else ... else ...", "All below-diagonal matrix coefficients vanish.", "external SchurTriangulation.lean:177-221", 30),
    spec("M0045-L-VV-ZERO", "core_lemma", "high", "In the V/V block, use the eigenvector equation and orthonormality to make below-diagonal coefficients zero.", "bV.orthonormal.right and f.HasEigenvector.apply_eq_smul", "The V/V below-diagonal entry is zero.", "external SchurTriangulation.lean:193-207", 44),
    spec("M0045-L-WV-ZERO", "core_lemma", "high", "In the W/V block, combine the eigenvector equation with membership in V orthogonal.", "V.inner_left_of_mem_orthogonal", "The W/V entry is zero.", "external SchurTriangulation.lean:193-211", 34),
    spec("M0045-L-WW-ZERO", "core_lemma", "critical", "In the W/W block, identify the coefficient with the compressed endomorphism and apply recursive triangularity after index subtraction.", "hg (Nat.sub_lt_sub_right ...)", "The W/W below-diagonal entry is zero.", "external SchurTriangulation.lean:212-221", 42),
    spec("M0045-L-INDEX-IMPOSSIBLE", "core_lemma", "normal", "Exclude a row in V with a strictly smaller column already outside V by transitivity of the finite order.", "hj (Nat.lt_trans hji hi)", "The impossible block-index branch is eliminated.", "external SchurTriangulation.lean:212-215", 14),
    spec("M0045-T-AUXILIARY", "terminal", "critical", "Package dimension equality, the assembled orthonormal basis, and all below-diagonal entry proofs into the recursive auxiliary result.", "LinearMap.SchurTriangulationAux.of", "An orthonormal basis whose matrix for f is BlockTriangular id.", "external SchurTriangulation.lean:107-114,173-237", 24),
    spec("M0045-C-MATRIX-BASIS", "construction", "critical", "Adapt the recursive auxiliary basis from the Euclidean endomorphism back to the original matrix index type.", "Matrix.schurTriangulationBasis", "An orthonormal basis indexed by the original matrix indices.", "external SchurTriangulation.lean:248-270", 34),
    spec("M0045-C-UNITARY", "construction", "critical", "Take the change-of-orthonormal-basis matrix and prove it belongs to Matrix.unitaryGroup.", "Matrix.schurTriangulationUnitary", "A unitary witness U.", "external SchurTriangulation.lean:267-276", 28),
    spec("M0045-C-TRIANGULAR", "construction", "critical", "Expose the matrix in the constructed basis as an upper-triangular matrix T.", "Matrix.schurTriangulation", "An upper-triangular witness T.", "external SchurTriangulation.lean:278-281", 18),
    spec("M0045-T-EQUATION", "terminal", "critical", "Use the change-of-basis matrix identity to prove A = U*T*star U.", "Matrix.schur_triangulation", "The exact factorization equation for A.", "external SchurTriangulation.lean:283-299", 38),
    spec("M0045-T-PACKAGE", "terminal", "critical", "Specialize the algebraically closed RCLike construction to Complex and Fin n and package U, T, unitarity, triangularity, and the equation for every A.", "Stage1Instances.THM_M_0045.ObligationTree.SchurEquationPackage", "A global SchurEquationPackage.", "planned current-pin port/integration of external Matrix.schur_triangulation", 32),
    spec("M0045-X-EXTERNAL-PORT", "bridge", "critical", "Port or immutably integrate the historical branch implementation and reproduce it at its own pins before current-pin use.", "external commit 0a539f0ce764fd16726509b62ed7b870461070eb", "A repo-local compatible or pinned external kernel artifact.", "external-anchor-snapshot.json; anchor-audit.json", 60),
    spec("M0045-X-SOURCE", "terminal", "high", "Map Schur 1909 and Axler Theorem 6.38 to each mathematical obligation, with definition transport, errata review, and independent approval.", "human-source crosswalk; no Lean proposition", "Human-source coverage without machine proof credit.", "source-statement-crosswalk.md", 80),
    spec("M0045-X-PROVENANCE", "certificate", "critical", "Track every wrapper, historical proof body, current-pin port, import, revision, license, declaration dependency, and evidence packet.", "content-addressed provenance closure", "Unambiguous terminal-body and artifact provenance.", "anchor-audit.json; external-anchor-snapshot.json", 60),
    spec("M0045-X-TRUST", "certificate", "critical", "Close transitive axioms, placeholders, unsafe/oracle paths, executables, compiled artifacts, toolchains, dependencies, replay, and supply-chain trust.", "release trust closure", "An accepted TCB and foundation record.", "anchor-audit.json trust_boundary; downstream validation", 60),
    spec("M0045-X-READABLE", "certificate", "high", "Produce an independently reviewed node-by-node reconstruction of the eigenspace descent and basis assembly, anchored to formal evidence.", "structured readable proof record", "R0-readable coverage for every required mathematical node.", "obligation-tree.md is architecture only; full reconstruction pending", 100),
]


# Parent-to-child proof requirements. Only the exact root adapter has a checked
# child-to-parent certificate in this phase. The other reverse edges truthfully
# remain logical decompositions of the immutable historical body.
REQUIRES = {
    "M0045-ROOT": ["M0045-T-PACKAGE"],
    "M0045-T-PACKAGE": ["M0045-T-EQUATION", "M0045-C-UNITARY", "M0045-C-TRIANGULAR", "M0045-S-DOMAIN"],
    "M0045-T-EQUATION": ["M0045-C-MATRIX-BASIS", "M0045-C-UNITARY", "M0045-C-TRIANGULAR"],
    "M0045-C-MATRIX-BASIS": ["M0045-T-AUXILIARY", "M0045-N-MATRIX-OPERATOR", "M0045-N-REINDEX"],
    "M0045-C-UNITARY": ["M0045-C-MATRIX-BASIS"],
    "M0045-C-TRIANGULAR": ["M0045-T-AUXILIARY", "M0045-C-MATRIX-BASIS"],
    "M0045-T-AUXILIARY": ["M0045-B-DIMENSION"],
    "M0045-B-DIMENSION": ["M0045-B-ZERO", "M0045-B-NONTRIVIAL"],
    "M0045-B-NONTRIVIAL": ["M0045-C-EIGENVALUE", "M0045-C-EIGENSPACE", "M0045-C-ORTHOGONAL", "M0045-C-COMPRESSED", "M0045-C-RECURSION", "M0045-L-DESCENT", "M0045-C-EIGENBASIS", "M0045-C-COMPLEMENT-BASIS", "M0045-C-INTERNAL-SUM", "M0045-C-COLLECTED-BASIS", "M0045-B-ENTRY-SPLIT"],
    "M0045-C-RECURSION": ["M0045-C-COMPRESSED", "M0045-L-DESCENT"],
    "M0045-C-COLLECTED-BASIS": ["M0045-C-EIGENBASIS", "M0045-C-COMPLEMENT-BASIS", "M0045-C-INTERNAL-SUM"],
    "M0045-B-ENTRY-SPLIT": ["M0045-L-VV-ZERO", "M0045-L-WV-ZERO", "M0045-L-WW-ZERO", "M0045-L-INDEX-IMPOSSIBLE"],
    "M0045-L-WW-ZERO": ["M0045-C-RECURSION"],
}

SOURCE_NA = {
    "M0045-S-FOUNDATION", "M0045-X-PROVENANCE", "M0045-X-TRUST", "M0045-X-READABLE",
}
MACHINE_SPECIAL = {
    "M0045-S-TARGET": "informational",
    "M0045-X-EXTERNAL-PORT": "informational",
    "M0045-X-SOURCE": "not_applicable",
    "M0045-X-PROVENANCE": "informational",
    "M0045-X-TRUST": "informational",
    "M0045-X-READABLE": "informational",
}
spec_by_id = {row["id"]: row for row in SPECS}
statement_expression_hash = "275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b"
CHECKED_TYPE_SHA256 = {
    "M0045-S-BOUNDARY": "0210febf045e66d390a1585ac6283173d053d538be2ab6299d934f71ebba7307",
    "M0045-S-EQUATION": "e2134253fa77c67f3e995dbeb74e134e2b41fa4caa65768c514abd475b826d89",
    "M0045-T-PACKAGE": "5b5118f95502e6cedc03fb2457663df2551eafff204674bcfe3c70ce25083383",
}


obligations = []
for row in SPECS:
    oid = row["id"]
    if oid in {"M0045-ROOT", "M0045-S-TARGET"}:
        fingerprint = "lean-expression-sha256:" + statement_expression_hash
    elif oid in CHECKED_TYPE_SHA256:
        fingerprint = "lean-pp-universes-output-sha256:" + CHECKED_TYPE_SHA256[oid]
    else:
        fingerprint = "architecture:v1:sha256:" + digest([
            oid, row["kind"], row["statement"], row["formal_target"], row["output"], row["source"]
        ])
    machine = MACHINE_SPECIAL.get(oid, "required")
    terminal_body = None
    recursive_body_nodes = {
        "M0045-B-DIMENSION", "M0045-B-ZERO", "M0045-B-NONTRIVIAL",
        "M0045-C-EIGENVALUE", "M0045-C-EIGENSPACE", "M0045-C-ORTHOGONAL",
        "M0045-C-COMPRESSED", "M0045-C-RECURSION", "M0045-L-DESCENT",
        "M0045-C-EIGENBASIS", "M0045-C-COMPLEMENT-BASIS", "M0045-C-INTERNAL-SUM",
        "M0045-C-COLLECTED-BASIS", "M0045-B-ENTRY-SPLIT", "M0045-L-VV-ZERO",
        "M0045-L-WV-ZERO", "M0045-L-WW-ZERO", "M0045-L-INDEX-IMPOSSIBLE",
        "M0045-T-AUXILIARY",
    }
    if oid in recursive_body_nodes:
        terminal_body = (
            "external-mathlib:" + EXTERNAL_REVISION
            + ":Mathlib.LinearAlgebra.Matrix.SchurTriangulation#private-LinearMap.SchurTriangulationAux.of"
        )
    elif oid == "M0045-C-MATRIX-BASIS":
        terminal_body = "external-mathlib:" + EXTERNAL_REVISION + "#Matrix.schurTriangulationBasis"
    elif oid == "M0045-C-UNITARY":
        terminal_body = "external-mathlib:" + EXTERNAL_REVISION + "#Matrix.schurTriangulationUnitary"
    elif oid == "M0045-C-TRIANGULAR":
        terminal_body = "external-mathlib:" + EXTERNAL_REVISION + "#Matrix.schurTriangulation"
    elif oid == "M0045-T-EQUATION":
        terminal_body = (
            "external-mathlib:" + EXTERNAL_REVISION
            + ":Mathlib.LinearAlgebra.Matrix.SchurTriangulation#Matrix.schur_triangulation"
        )
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": row["kind"],
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in SOURCE_NA else "required",
        "readable_eligibility": "required",
        "risk_class": row["risk"],
        "exclusion_reason": (
            "human_source_boundary_only" if machine == "not_applicable"
            else "target_interface_overlay_no_duplicate_root_proof_credit"
            if oid == "M0045-S-TARGET"
            else "support_overlay_no_machine_proof_credit" if machine == "informational"
            else "foundation_boundary_no_human_mathematical_source_credit"
            if oid == "M0045-S-FOUNDATION" else None
        ),
        "terminal_proof_body_id": terminal_body,
    })

DENOMINATOR_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
denominator = digest([{key: row[key] for key in DENOMINATOR_FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "registry_id": "THM-M-0045-OBLIGATIONS-v1",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-13T00:00:00+08:00",
    "freeze_basis": "The exact elaborated statement, bounded anchor inventory, and full architecture of immutable external source 0a539f0c determine the recursive eigenspace, orthogonal-complement, basis-assembly, matrix-transport, equation, source, provenance, trust, and readability obligations. Eligibility was assigned before recording closure status.",
    "frozen_against_statement_sha256": file_sha256("Statement.lean"),
    "frozen_against_anchor_audit_sha256": file_sha256("anchor-audit.json"),
    "frozen_external_source_revision": EXTERNAL_REVISION,
    "frozen_external_source_sha256": EXTERNAL_SOURCE_SHA256,
    "root_obligation_id": "M0045-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
    },
    "layer_exclusions": {
        "computation": {
            "status": "not_applicable_pending_independent_approval",
            "reason": "The exact theorem is mathematical existence. No numerical Schur algorithm, floating-point tolerance, solver, reflection, oracle, or finite certificate is credited.",
        }
    },
    "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, or terminal-body identity change requires registry version 2 and an append-only old/new semantic-ID delta.",
    "append_only_delta": [],
    "obligations": obligations,
    "status_observed_after_freeze": {
        "closed_obligations": [],
        "accepted_root_machine_debt": "M3",
        "external_candidate": "0a539f0c remains M5/E3: incompatible with the current pin and without own-pin kernel/trust evidence.",
        "human_source_debt": "H1",
        "readability_debt": "R4",
    },
    "status_boundary": "Frozen architecture only. No obligation is accepted closed; the historical proof body remains outside the dependency closure, and the current classified root remains H1/M3/R4.",
}


def semantic_ledger(row: dict) -> list[dict]:
    oid = row["id"]
    children = REQUIRES.get(oid, [])
    steps = []
    for index, child in enumerate(children, 1):
        steps.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": [child],
            "inference": "Consume the exact output of the declared proof child.",
            "source_locator": spec_by_id[child]["source"],
            "output": spec_by_id[child]["output"],
            "outgoing_use": f"planned child-to-parent composition for {oid}",
        })
    steps.append({
        "step_id": f"{oid}-STEP-{len(steps) + 1:02d}",
        "premise_ids": children if children else ["frozen-formal-context"],
        "inference": row["formal_target"],
        "source_locator": row["source"],
        "output": row["output"],
        "outgoing_use": "Declared proof parent or a typed non-proof support edge only.",
    })
    return steps


# Exact leaf ledgers from the frozen target, checked interface, historical body,
# and audit artifacts. These are mathematical transitions, not generated filler.
LEAF_LEDGERS = {
    "M0045-S-TARGET": [
        (["frozen-formal-context"], "Read the ordered universal n and A binders and existential U binder from the elaborated declaration.", "Statement.lean:16-21", "The exact binder context."),
        (["M0045-S-TARGET-STEP-01"], "Retain unitary membership and BlockTriangular (star U * A * U) id conjuncts without strengthening or omission.", "statement.json canonical_formal_target", "The exact root interface."),
    ],
    "M0045-S-DOMAIN": [
        (["frozen-formal-context"], "Instantiate square matrices at Fin n over Complex with the canonical finite order and decidable equality.", "Statement.lean:17-21", "Matrix (Fin n) (Fin n) Complex for arbitrary n."),
        (["M0045-S-DOMAIN-STEP-01"], "Keep n universally quantified, including zero, rather than replacing Fin n by an unrelated finite index type.", "BoundaryProbe.lean:14-31", "The root's exact domain and typeclass context."),
    ],
    "M0045-S-BOUNDARY": [
        (["frozen-formal-context"], "Apply Nat.eq_zero_or_pos to an arbitrary matrix dimension.", "ObligationTree.lean:dimensionBoundary", "n = 0 or 0 < n."),
        (["M0045-S-BOUNDARY-STEP-01"], "Use the identity witness probes at dimensions zero and one to confirm neither case was excluded.", "BoundaryProbe.lean:14-31", "Every natural dimension remains in the target family."),
    ],
    "M0045-S-EQUATION": [
        (["frozen-formal-context"], "Use unitary membership to derive star U * U = 1.", "Matrix.mem_unitaryGroup_iff'; ObligationTree.lean", "The left inverse equation for U."),
        (["M0045-S-EQUATION-STEP-01"], "Rewrite A = U*T*star U and reassociate the two conjugating products.", "ObligationTree.lean:equationWitness_implies_targetAt", "star U * A * U = (star U*U)*T*(star U*U)."),
        (["M0045-S-EQUATION-STEP-02"], "Reduce both unitary products to one and transport BlockTriangular T id across the equality.", "ObligationTree.lean:equationWitness_implies_targetAt", "BlockTriangular (star U * A * U) id."),
    ],
    "M0045-S-FOUNDATION": [
        (["frozen-formal-context"], "Elaborate the exact conditional transport and root adapter at the pinned Lean/mathlib revisions.", "ObligationTree.lean axiom probes", "Two checked declarations at the current pin."),
        (["M0045-S-FOUNDATION-STEP-01"], "Inspect their kernel axiom reports and exclude placeholder, unsafe, oracle, and numerical-computation credit.", "check_obligation_tree.py; #print axioms", "Observed propext, Classical.choice, and Quot.sound only."),
    ],
    "M0045-N-MATRIX-OPERATOR": [
        (["frozen-formal-context"], "Convert A to its Euclidean-space endomorphism with Matrix.toEuclideanLin.", "external SchurTriangulation.lean:252-255", "An endomorphism f representing A."),
        (["M0045-N-MATRIX-OPERATOR-STEP-01"], "Represent f in the constructed orthonormal basis using LinearMap.toMatrixOrthonormal.", "external SchurTriangulation.lean:258-265", "The triangular matrix B for the same endomorphism."),
        (["M0045-N-MATRIX-OPERATOR-STEP-02"], "Use toLin/toMatrix identities to recover A in the standard Euclidean basis.", "external SchurTriangulation.lean:288-295", "The matrix change-of-basis identity used in the final equation."),
    ],
    "M0045-N-REINDEX": [
        (["frozen-formal-context"], "Use finrank equality to construct Fintype.orderIsoFinOfCardEq between Fin d and the original index type.", "external SchurTriangulation.lean:255-257", "An order isomorphism e : Fin d equiv_o n."),
        (["M0045-N-REINDEX-STEP-01"], "Reindex the recursive orthonormal basis along e and transport matrix coefficients through toMatrixOrthonormal_reindex.", "external SchurTriangulation.lean:257-265", "An original-index basis preserving upper triangularity."),
    ],
    "M0045-B-ZERO": [
        (["frozen-formal-context"], "Turn not Nontrivial E into a Subsingleton E instance.", "external SchurTriangulation.lean:223-224", "A subsingleton inner-product space."),
        (["M0045-B-ZERO-STEP-01"], "Apply finrank_zero_of_subsingleton and select the empty orthonormal basis.", "external SchurTriangulation.lean:225-229", "Dimension zero and an orthonormal basis indexed by Fin 0."),
        (["M0045-B-ZERO-STEP-02"], "Discharge below-diagonal triangularity by empty elimination.", "external SchurTriangulation.lean:229", "The zero-dimensional auxiliary package."),
    ],
    "M0045-C-EIGENVALUE": [
        (["frozen-formal-context"], "Use algebraic closedness and nontriviality to inhabit f.Eigenvalues.", "Module.End.exists_eigenvalue; external source:155", "A selected eigenvalue mu."),
        (["M0045-C-EIGENVALUE-STEP-01"], "Retain the subtype property witnessing a nonzero eigenvector for mu.", "external source:200-202,236", "The nontrivial eigenvalue witness used by descent."),
    ],
    "M0045-C-EIGENSPACE": [
        (["M0045-C-EIGENVALUE"], "Define V as f.eigenspace mu.", "external source:156", "An f-invariant submodule V."),
        (["M0045-C-EIGENSPACE-STEP-01"], "Place the selected eigenvector in V and use its nonzeroness.", "external source:200-202", "V is nontrivial."),
        (["M0045-C-EIGENSPACE-STEP-02"], "Convert nontriviality to 0 < finrank K V.", "Submodule.one_le_finrank_iff; external source:236", "Positive finrank for the descent argument."),
    ],
    "M0045-C-ORTHOGONAL": [
        (["M0045-C-EIGENSPACE"], "Define W as the orthogonal complement of V.", "external source:157", "Submodule W = V orthogonal."),
        (["M0045-C-ORTHOGONAL-STEP-01"], "Use V.orthogonalFamily_self and completeness to prove V sup W = top.", "external source:164-167", "An orthogonal family spanning E."),
        (["M0045-C-ORTHOGONAL-STEP-02"], "Build DirectSum.IsInternal for the Boolean family selecting V or W.", "external source:165-170", "The internal direct-sum decomposition E = V direct-sum W."),
    ],
    "M0045-C-COMPRESSED": [
        (["M0045-C-ORTHOGONAL"], "Restrict f to W using domRestrict.", "external source:160", "A linear map W -> E."),
        (["M0045-C-COMPRESSED-STEP-01"], "Compose with orthogonalProjection W to return to W.", "external source:160", "The compressed endomorphism g : Module.End K W."),
    ],
    "M0045-L-DESCENT": [
        (["M0045-C-EIGENSPACE"], "Use positive finrank V to prove finrank W < finrank V + finrank W.", "external source:233-236", "A strict inequality below the direct-sum dimension."),
        (["M0045-L-DESCENT-STEP-01", "M0045-C-ORTHOGONAL"], "Rewrite finrank V + finrank W as finrank E by orthogonal finrank additivity.", "external source:159,237", "finrank W < finrank E."),
    ],
    "M0045-C-EIGENBASIS": [
        (["M0045-C-EIGENSPACE"], "Apply stdOrthonormalBasis to the finite-dimensional eigenspace V.", "external source:163", "bV : OrthonormalBasis (Fin (finrank K V)) K V."),
        (["M0045-C-EIGENBASIS-STEP-01"], "Retain bV orthonormality and basis-vector nonzeroness for the V-block coefficient proof.", "external source:200-207", "The eigenbasis invariants consumed by V/V and W/V cases."),
    ],
    "M0045-C-COMPLEMENT-BASIS": [
        (["M0045-C-RECURSION"], "Project the recursive result fields for the compressed endomorphism g.", "external source:161", "Dimension n, equality hn, basis bW, and triangularity hg."),
        (["M0045-C-COMPLEMENT-BASIS-STEP-01"], "Retain bW vectors in W and hg for the W/W block.", "external source:168,209-221", "The complement basis invariants."),
    ],
    "M0045-C-INTERNAL-SUM": [
        (["M0045-C-ORTHOGONAL"], "Combine orthogonality with V sup W = top.", "external source:164-167", "A complete orthogonal two-submodule family."),
        (["M0045-C-INTERNAL-SUM-STEP-01"], "Apply the orthogonal decomposition's isInternal theorem.", "external source:165-170", "DirectSum.IsInternal (cond . V W)."),
    ],
    "M0045-L-VV-ZERO": [
        (["M0045-C-EIGENBASIS"], "For j < i in V, use the eigenvector equation f(bV j) = mu*bV j.", "external source:193-202", "The coefficient is mu times inner (bV i) (bV j)."),
        (["M0045-L-VV-ZERO-STEP-01"], "Apply orthonormality at distinct indices.", "external source:204-207", "The V/V below-diagonal coefficient is zero."),
    ],
    "M0045-L-WV-ZERO": [
        (["M0045-C-EIGENBASIS", "M0045-C-COMPLEMENT-BASIS"], "Rewrite f(bV j) by the eigenvector equation.", "external source:193-202", "The W/V coefficient reduces to inner (bW i) (bV j)."),
        (["M0045-L-WV-ZERO-STEP-01", "M0045-C-ORTHOGONAL"], "Use bW membership in V orthogonal and bV membership in V.", "external source:208-211", "The W/V below-diagonal coefficient is zero."),
    ],
    "M0045-L-INDEX-IMPOSSIBLE": [
        (["frozen-formal-context"], "Assume the row lies in V while the smaller column does not.", "external source:212-215", "i < m, not j < m, and j < i."),
        (["M0045-L-INDEX-IMPOSSIBLE-STEP-01"], "Apply transitivity j < i < m, contradicting not j < m.", "external source:213", "The impossible block-index case is eliminated."),
    ],
    "M0045-X-EXTERNAL-PORT": [
        (["frozen-formal-context"], "Authenticate external commit, tree, source blob/hash, toolchain file, manifest, and license from already materialized Git objects.", "external-anchor-snapshot.json", "An immutable E3 source identity."),
        (["M0045-X-EXTERNAL-PORT-STEP-01"], "Replay the historical source against the current pin and retain the concrete API incompatibility diagnostics.", "anchor-audit-validation.md", "A current-pin integration failure, not proof evidence."),
        (["M0045-X-EXTERNAL-PORT-STEP-02"], "Require own-pin kernel/trust replay followed by current-pin port or immutable integration before closure.", "anchor-audit.json reopen_when", "The exact actionable port gate."),
    ],
    "M0045-X-SOURCE": [
        (["frozen-formal-context"], "Pin Schur 1909 Satz I and Axler 4e Theorem 6.38 with their stated triangular conventions.", "source-statement-crosswalk.md", "Two H1 source leads."),
        (["M0045-X-SOURCE-STEP-01"], "Leave definition transport, errata, archival preservation, node mapping, and independent review explicit.", "source-statement-crosswalk.md open requirements", "An H1 boundary rather than H0 credit."),
    ],
    "M0045-X-PROVENANCE": [
        (["frozen-formal-context"], "Bind the local target/adapter hashes and external commit/tree/blob/license identities.", "anchor-audit.json; external-anchor-snapshot.json", "Partial wrapper/body/conclusion provenance."),
        (["M0045-X-PROVENANCE-STEP-01"], "Keep the absent own-pin artifact, terminal dependency closure, and current-pin port distinct.", "anchor-audit.json trust_boundary", "An open provenance closure record."),
    ],
    "M0045-X-TRUST": [
        (["frozen-formal-context"], "Record current-pin adapter axioms and prohibited-token result separately from the historical source scan.", "AnchorAudit.lean; ObligationTree.lean; external-anchor-snapshot.json", "Local E2-style interface evidence and external E3 text evidence."),
        (["M0045-X-TRUST-STEP-01"], "Require historical own-pin axioms/placeholders/unsafe closure plus current-pin dependency and replay evidence.", "anchor-audit.json reopen_when", "The open release trust cut."),
    ],
    "M0045-X-READABLE": [
        (["frozen-formal-context"], "Expose every recursive construction, branch, transport, and terminal boundary as a stable public node.", "obligation-tree.md", "An architecture-readable node map."),
        (["M0045-X-READABLE-STEP-01"], "Leave source-faithful derivation details and independent review uncredited.", "README.md; source-statement-crosswalk.md", "R4 remains open; this architecture is not R0."),
    ],
}


def final_ledger(row: dict) -> list[dict]:
    oid = row["id"]
    if oid not in LEAF_LEDGERS:
        return semantic_ledger(row)
    result = []
    entries = LEAF_LEDGERS[oid]
    for index, (premises, inference, locator, step_output) in enumerate(entries, 1):
        result.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": premises,
            "inference": inference,
            "source_locator": locator,
            "output": step_output,
            "outgoing_use": row["output"] if index == len(entries) else f"{oid}-STEP-{index + 1:02d}",
        })
    return result


nodes = []
for row, obligation in zip(SPECS, obligations):
    oid = row["id"]
    if oid == "M0045-X-EXTERNAL-PORT":
        machine_debt = "M5"
    elif oid in {"M0045-ROOT", "M0045-S-TARGET", "M0045-S-DOMAIN", "M0045-S-BOUNDARY", "M0045-S-EQUATION", "M0045-S-FOUNDATION"}:
        machine_debt = "M3"
    elif obligation["machine_eligibility"] in {"not_applicable", "informational"}:
        machine_debt = "M5"
    else:
        machine_debt = "M4"
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
        "obligation_id": oid,
        "kind": row["kind"],
        "human_statement": row["statement"],
        "formal_target": row["formal_target"],
        "output": row["output"],
        "human_debt": "H1" if obligation["human_source_eligibility"] == "required" else "H2",
        "machine_debt": machine_debt,
        "readability_debt": "R4",
        "evidence_ids": ["M0045-A-MATHLIB-BRANCH-SCHUR-E3-UNACCEPTED"] if oid not in SOURCE_NA else [],
        "source_crosswalk_id": "SRC-M0045-SCHUR1909-AXLER4E-PARTIAL" if obligation["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0045-EXTERNAL-0A539F0C-PARTIAL" if oid not in SOURCE_NA else "none",
        "foundation_profile": "Lean4-mathlib-classical candidate; propext, Classical.choice, Quot.sound observed; acceptance open",
        "tcb_profile": "Lean-4.29.0+mathlib-8a178386 local adapter; historical Lean-v4.17.0-rc1 source body outside closure; transitive trust open",
        "computation_record": "none; no numerical algorithm, solver, oracle, reflection, or unchecked certificate closes this node",
        "step_budget": row["budget"],
        "semantic_step_ledger": final_ledger(row),
        "public_readable_target": f"Stage1_Instances/THM-M-0045/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0045-OBLIGATION-BUNDLE",
        "status_boundary": "Frozen architecture and unaccepted E3 source mapping only; no M0, E1/E2, H0, R0, proof acceptance, audit completion, or theorem completion is credited.",
        "task_ids": [ITEM],
        "owned_sources": ["Stage1_Instances/THM-M-0045/ObligationTree.lean"] if oid in {"M0045-ROOT", "M0045-S-EQUATION"} else [],
        "owner": "THM-M-0045 execution lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-13",
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement hash", "anchor hash", "registry hash", "external source revision/hash", "toolchain/dependency pins", "composition source"],
            "revocation_state": "not-accepted",
        },
    })


def edge(eid: str, source: str, kind: str, target: str, reciprocal: str | None = None) -> dict:
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


proof_edges = []
internal_refinement_edges = []
for parent, children in REQUIRES.items():
    for child in children:
        if parent == "M0045-ROOT":
            req = "REQ-" + parent + "-" + child
            rev = "CMP-" + child + "-" + parent
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, rev),
                edge(rev, child, "composes", parent, req),
            ])
        else:
            internal_refinement_edges.append(
                edge("DECOMPOSE-" + parent + "-" + child, parent, "logical_decomposition", child)
            )

workflow_tasks = [
    "S56-M-0045-ANCHOR_AUDIT", ITEM, "S56-M-0045-PROOF",
    "S56-M-0045-VALIDATION", "S56-M-0045-RELEASE",
]
graph_edges = {
    "proof": proof_edges,
    "refinement": [
        edge("REF-ROOT-TARGET", "M0045-ROOT", "logical_decomposition", "M0045-S-TARGET"),
        edge("REF-ROOT-DOMAIN", "M0045-ROOT", "logical_decomposition", "M0045-S-DOMAIN"),
        edge("REF-ROOT-BOUNDARY", "M0045-ROOT", "logical_decomposition", "M0045-S-BOUNDARY"),
        edge("REF-ROOT-EQUATION", "M0045-ROOT", "transports", "M0045-S-EQUATION"),
    ] + internal_refinement_edges,
    "provenance": [],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUNDATION", "M0045-ROOT", "trusts", "M0045-S-FOUNDATION"),
        edge("TRUST-EXTERNAL", "M0045-ROOT", "trusts", "M0045-X-EXTERNAL-PORT"),
        edge("TRUST-RELEASE", "M0045-ROOT", "trusts", "M0045-X-TRUST"),
    ],
    "documentation": [],
    "workflow": [
        edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0045-ANCHOR_AUDIT"),
        edge("FLOW-PROOF-TREE", "S56-M-0045-PROOF", "workflow_depends_on", ITEM),
        edge("FLOW-VALIDATION-PROOF", "S56-M-0045-VALIDATION", "workflow_depends_on", "S56-M-0045-PROOF"),
        edge("FLOW-RELEASE-VALIDATION", "S56-M-0045-RELEASE", "workflow_depends_on", "S56-M-0045-VALIDATION"),
    ],
}

for oid in ids:
    obligation = next(row for row in obligations if row["obligation_id"] == oid)
    if oid != "M0045-X-SOURCE" and obligation["human_source_eligibility"] == "required":
        graph_edges["provenance"].append(edge("SOURCE-MAP-" + oid, oid, "source_map", "M0045-X-SOURCE"))
    if oid not in {"M0045-X-SOURCE", "M0045-X-PROVENANCE", "M0045-X-TRUST", "M0045-X-READABLE"}:
        graph_edges["provenance"].append(edge("PROVENANCE-" + oid, "M0045-X-PROVENANCE", "provenance_of", oid))
    if oid != "M0045-X-READABLE":
        graph_edges["documentation"].append(edge("DOCUMENT-" + oid, "M0045-X-READABLE", "documents", oid))

# These edges record pending integration evidence requirements. Their open E3
# node is not a content-addressed acceptance packet and closes nothing.
graph_edges["evidence"] = [
    edge("EVIDENCE-E3-PORT", "M0045-X-EXTERNAL-PORT", "evidence_for", "M0045-T-PACKAGE"),
    edge("EVIDENCE-E3-EQUATION", "M0045-X-EXTERNAL-PORT", "evidence_for", "M0045-T-EQUATION"),
]

graphs = {}
for name, entries in graph_edges.items():
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for entry in entries:
        outgoing.setdefault(entry["from"], []).append(entry["edge_id"])
        incoming.setdefault(entry["to"], []).append(entry["edge_id"])
    graphs[name] = {"edges": entries, "out": outgoing, "in": incoming}

composition_certificates = [{
    "certificate_id": "COMP-M0045-ROOT",
    "parent_obligation_id": "M0045-ROOT",
    "parent_statement_fingerprint": next(row["statement_fingerprint"] for row in obligations if row["obligation_id"] == "M0045-ROOT"),
    "required_child_ids": ["M0045-T-PACKAGE"],
    "required_child_statement_fingerprints": {
        "M0045-T-PACKAGE": next(row["statement_fingerprint"] for row in obligations if row["obligation_id"] == "M0045-T-PACKAGE")
    },
    "checked_declaration": "Stage1Instances.THM_M_0045.ObligationTree.root_of_equationPackage",
    "certificate_kind": "lean_abstract_child_harness",
    "status": "provisionally_elaborated_not_accepted",
    "introduces_undeclared_premises": False,
}]
unverified_plans = []
for parent, children in REQUIRES.items():
    if parent == "M0045-ROOT":
        continue
    unverified_plans.append({
        "plan_id": "DECOMP-" + parent,
        "parent_obligation_id": parent,
        "planned_child_ids": children,
        "source_declaration": "historical external Matrix.schur_triangulation / LinearMap.SchurTriangulationAux.of",
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact current-pin abstract-child harness must bind the frozen fingerprints and consume every child before this parent may close.",
    })

proof_children = {child for children in REQUIRES.values() for child in children}
proof_parents = set(REQUIRES)
proof_leaf_cut_set = sorted(proof_children - proof_parents)
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": registry["registry_id"],
    "registry_denominator_sha256": denominator,
    "root_node_id": "THM-M-0045-ROOT",
    "edge_endpoint_namespace": "canonical obligation_id except the workflow graph, which uses declared task IDs",
    "edge_direction": "Proof requirements run parent to child; reciprocal checked composes or unverified logical_decomposition edges run child to parent. Workflow dependencies run task to prerequisite.",
    "workflow_task_nodes": workflow_tasks,
    "nodes": nodes,
    "graphs": graphs,
    "composition_certificates": composition_certificates,
    "unverified_decomposition_plans": unverified_plans,
    "closure_boundary": {
        "closed_obligations": [],
        "root_closed": False,
        "accepted_root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "proof_leaf_cut_set": ["M0045-T-PACKAGE"],
        "historical_route_leaf_cut_set": proof_leaf_cut_set,
        "remaining_root_cut_set": ["M0045-T-PACKAGE"],
        "remaining_release_cut_set": ["M0045-X-SOURCE", "M0045-X-PROVENANCE", "M0045-X-TRUST", "M0045-X-READABLE", "hermetic replay", "independent verification", "master acceptance"],
        "distinct_known_terminal_body_ids": sorted({
            row["terminal_proof_body_id"] for row in obligations
            if row["terminal_proof_body_id"] is not None
        }),
        "candidate_evidence": "The historical source is M5/E3, not an accepted machine proof. Only the root's conditional equation-package adapter is kernel-checked here.",
        "reason": "The immediate proof cut is the global equation package. Porting the historical source is one planned implementation route, not a logically necessary premise: a fresh current-pin proof could also close the package. Every historical internal source decomposition still needs an exact current-pin composition certificate before that route receives credit.",
    },
}

recipes = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{
        "recipe_id": "VAL-M0045-OBLIGATION-BUNDLE",
        "cwd": ".",
        "argv": ["python3", "-B", "Stage1_Instances/THM-M-0045/check_obligation_tree.py"],
        "env_allowlist": {
            "PATH": "runner-provided tool path",
            "HOME": "runner-provided toolchain home",
            "TMPDIR": "runner-provided temporary directory",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        "timeout_seconds": 180,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [
            {"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0045 obligation tree with obligation, edge, and ledger counts"},
            {"path_or_stream": "stdout", "semantic_hash_policy": "contains root closure: open (H1/M3/R4) and theorem_complete=false"},
        ],
        "covered_obligation_ids": ids,
        "covered_declarations": [
            "Stage1Instances.THM_M_0045.SchurTriangularizationTarget",
            "Stage1Instances.THM_M_0045.ObligationTree.SchurEquationPackage",
            "Stage1Instances.THM_M_0045.ObligationTree.equationWitness_implies_targetAt",
            "Stage1Instances.THM_M_0045.ObligationTree.root_of_equationPackage",
        ],
        "coverage_boundary": "The checker structurally covers the entire frozen architecture, but kernel coverage is limited to the exact target, equation-package interface, and conditional root composition. The historical source body and internal child-to-parent compositions remain open.",
    }],
}

markdown = [
    "# THM-M-0045 frozen obligation architecture",
    "",
    f"Item: `{ITEM}`.",
    "",
    f"Registry version 1 freezes {len(ids)} semantic obligations before any proof-phase closure credit.",
    "The proof graph expands the immutable 300-line historical Schur source through its eigenspace",
    "descent, orthogonal-complement recursion, collected orthonormal basis, block-entry cases, matrix",
    "transport, unitary witness, triangular witness, and final factorization. Provenance, evidence,",
    "trust, documentation, and workflow edges are separate and cannot act as proof premises.",
    "",
    "## Proof route",
    "",
    "```text",
    "ROOT <- checked conditional adapter <- equation package",
    "  <- unitary U + upper triangular T + A = U*T*star U",
    "  <- matrix/endomorphism transport + recursive auxiliary basis",
    "  <- zero/nontrivial dimension split",
    "     nontrivial <- eigenvalue/eigenspace V + W = V orthogonal",
    "       <- compressed restriction on W + strict finrank descent",
    "       <- recursive basis on W + eigenbasis on V + internal direct sum",
    "       <- V/V, W/V, W/W, and impossible block-entry cases",
    "```",
    "",
    "Only the first arrow is a checked current-pin composition certificate. Every internal reverse",
    "edge is explicitly `logical_decomposition` until a current-pin abstract-child harness consumes",
    "all of its frozen children.",
    "",
    "## Node ledger",
    "",
]
for row in SPECS:
    markdown.extend([
        f"### {row['id'].lower()}",
        "",
        row["statement"],
        "",
        f"Formal target: `{row['formal_target']}`. Output: {row['output']}",
        f"Source boundary: {row['source']}. Budget: {row['budget']} substantive steps maximum; structured ledger: {len(final_ledger(row))} recorded step(s).",
        "",
    ])
markdown.extend([
    "## Freeze boundary",
    "",
    "No obligation is accepted closed. External revision `0a539f0c` remains `M5/E3`: it is outside",
    "the repository dependency closure, fails at the current pin, and has no own-pin kernel, axiom,",
    "placeholder, unsafe, or transitive trust receipt. The root remains accepted `[H1, M3, R4]`.",
    "Primary-source H0, readable R0, compatible integration, all internal composition certificates,",
    "provenance/TCB closure, hermetic replay, independent verification, audit completion, theorem",
    "completion, and master acceptance remain open.",
    "",
])

outputs = {
    "obligation-registry.json": json.dumps(registry, indent=2, ensure_ascii=True) + "\n",
    "typed-graphs.json": json.dumps(bundle, indent=2, ensure_ascii=True) + "\n",
    "validation-specs.json": json.dumps(recipes, indent=2, ensure_ascii=True) + "\n",
    "obligation-tree.md": "\n".join(markdown),
}
for name, content in outputs.items():
    (HERE / name).write_text(content, encoding="utf-8")

edge_count = sum(len(graph["edges"]) for graph in graphs.values())
ledger_count = sum(len(node["semantic_step_ledger"]) for node in nodes)
print(f"wrote {len(ids)} obligations, {edge_count} typed edges, and {ledger_count} ledger steps")
print(f"registry denominator sha256: {denominator}")
