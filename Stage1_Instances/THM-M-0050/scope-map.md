# Scope map

## Preserved catalog boundary

- Stable ID: `THM-M-0050`; item: `S56-M-0050-INTAKE`; execution rank: 1089.
- Literal claim: `实对称矩阵正负惯性指数在合同下不变`.
- Faithful English gloss: the positive and negative inertia indices of a real symmetric matrix are
  invariant under congruence.
- The target is finite real symmetric matrix congruence invariance. This intake does not silently
  replace it with a broader Hermitian or abstract quadratic-space theorem.

## Decisions required at the statement gate

| Surface | Open decision and why it changes the proposition |
|---|---|
| Matrix domain | Choose `Matrix (Fin n) (Fin n) Real` or matrices over an arbitrary finite index type; fix universes and typeclass binders. |
| Symmetry | State `A.IsSymm` and `B.IsSymm`, or use a bundled symmetric matrix; do not let `toQuadraticMap'` erase a skew part silently. |
| Congruence | Define the invertible witness and exact orientation, for example `B = P.transpose * A * P`; decide GL element, matrix `Invertible`, or linear equivalence. |
| Inertia indices | Select eigenvalue multiplicity counts, signs in a congruent diagonal form, or maximal definite-subspace dimensions (`sigPos` and `sigNeg`). |
| Conclusion | Freeze equality of the positive and negative pair and decide whether equality of the zero index/nullity is explicit or derived. |
| Matrix transport | Prove the exact relationship between symmetric matrices, `Matrix.toQuadraticMap'`, `QuadraticMap.Equivalent`, and the selected index definitions. |
| Source scope | Ratify an exact real statement and its relationship to Treil's Hermitian formulation and the historical 1852 lead. |
| Foundation | Record classical choice/basis or eigenvalue selection, minimal imports, TCB, and axiom policy after the target is fixed. |

## Boundary cases to decide

The source review must explicitly cover zero-by-zero and one-by-one matrices, zero and singular
matrices, positive and negative definite matrices, indefinite matrices, repeated and zero
eigenvalues, identity/permutation congruences, and congruences of degenerate forms. Intake excludes
none of these. Restricting to invertible forms would be a weakened substitution.

## Formal surfaces, not proof credit

- `QuadraticMap.Equivalent.sigPos_eq` and `.sigNeg_eq` give the abstract equivalence-invariance
  interface.
- `QuadraticForm.sigPos_of_equiv_weightedSumSquares` and `.sigNeg_of_equiv_weightedSumSquares`
  connect signature to positive and negative weights.
- `QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared` supplies real diagonalization.
- `Matrix.toQuadraticMap'` and `QuadraticMap.toMatrix'_comp` expose the matrix congruence shape.
- `Matrix.IsSymm` exposes the literal matrix hypothesis.

These declarations are discovery evidence only. No exact matrix theorem, checked bidirectional
transport, normalized expression, proof-body provenance, or axiom report is accepted at intake.

## Explicit non-substitutions

Diagonalization existence, the spectral theorem, similarity invariance, SVD, Schur form,
positive-definite preservation, determinant sign, and rank invariance do not prove the requested
inertia invariance. Neither a nondegenerate-only theorem nor complex Hermitian inertia may replace
the literal real symmetric claim. An abstract quadratic-form theorem may be credited only after a
source-approved, kernel-checked transport.

## Neighbor boundary

`THM-M-0043` (spectral theorem) can support eigenvalue interpretation but is not uniqueness under
general congruence. `THM-M-0044` (SVD) is a two-sided factorization. `THM-M-0045` (Schur) is
triangularization. None inherits status into this target.
