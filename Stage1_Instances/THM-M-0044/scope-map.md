# THM-M-0044 scope map

## Human claim selected at intake

For a finite `m`-by-`n` matrix `A` over `R` or `C`, there should exist an `m`-by-`m` orthogonal or
unitary matrix `U`, an `n`-by-`n` orthogonal or unitary matrix `V`, and an `m`-by-`n` rectangular
diagonal matrix `Sigma`, with nonnegative real diagonal entries embedded in the scalar field, such
that `A = U * Sigma * V*`.

This is a conventional full-SVD reading of the catalog gloss, not an accepted source statement and
not a Lean target. The statement phase may change representation details only through an explicit,
source-faithful crosswalk and checked transports.

## Scope decisions

| Surface | Intake-selected meaning | Open verification |
|---|---|---|
| Scalars | real or complex numbers | one polymorphic `RCLike` statement versus separate real/complex roots |
| Matrix | arbitrary finite rectangular `m`-by-`n` matrix | exact finite index types, universe and decidable-equality binders |
| Left factor | square orthogonal/unitary `m`-by-`m` matrix | predicate/subtype representation and multiplication orientation |
| Right factor | square orthogonal/unitary `n`-by-`n` matrix | whether the witness is `V`, `V*`, or a basis-change equivalence |
| Middle factor | rectangular diagonal `m`-by-`n` matrix | precise off-diagonal predicate, padding, indexing, and scalar embedding |
| Diagonal entries | nonnegative singular values | ordering, multiplicity, and zero-padding convention |
| Conclusion | exact equality `A = U * Sigma * V*` | checked relationship to the linear-map orthonormal-list formulation |

## Boundary cases

- Empty row or column index types, including the `0`-by-`n`, `m`-by-`0`, and `0`-by-`0` cases,
  remain provisionally included. The statement gate must verify that the chosen rectangular
  diagonal and unitary conventions make these cases meaningful.
- The zero matrix, rank-deficient matrices, repeated singular values, square matrices, row vectors,
  column vectors, and wide or tall matrices remain in scope.
- A full SVD is selected provisionally. Thin/economy and compact rank-indexed SVDs are candidate
  alternate encodings, not replacements unless both required directions are checked.
- Ordering singular values decreasingly is useful for a canonical `Sigma`, but is not necessary for
  bare existence. The statement phase must say whether ordering is part of the exact conclusion.
- Infinite-dimensional compact-operator Schmidt decompositions are outside this matrix target.

## Non-substitution rules

- Do not replace arbitrary rectangular matrices by square, invertible, normal, Hermitian,
  positive-semidefinite, diagonalizable, fixed-size, real-only, or complex-only matrices.
- Do not replace SVD by the spectral theorem for `Aᴴ A`, the existence or properties of singular
  values, polar decomposition, QR decomposition, or diagonalization of a Hermitian matrix alone.
- Do not hide the missing left singular vectors or kernel/range completion inside a structure that
  assumes the desired factorization.
- Do not replace exact equality with an approximate numerical factorization, an algorithm run, or
  a floating-point residual.
- Do not transfer source, formal, or status credit from duplicate catalog target `THM-M-1449`.
- Do not treat the catalog's verified label, a successful `#check`, or an axiom report as proof
  completion.

## Downstream handoff

The statement phase must admit and independently review a pinpoint source; freeze field, index,
factor-shape, unitary, star, rectangular-diagonal, nonnegativity, ordering, and boundary conventions;
elaborate a minimal-import target; record expression and environment fingerprints; check credited
matrix/linear-map and full/thin transports; and execute the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations. Only later phases may audit proof-body
provenance, freeze obligations, implement proof work, or claim kernel closure.
