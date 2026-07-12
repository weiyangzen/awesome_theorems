# THM-M-0046 scope map

## Preserved theorem family

The intake preserves the finite real-or-complex QR factorization family indicated by the catalog:
a matrix factors exactly as `A = Q * R`, with an orthogonal/unitary or column-orthonormal factor
`Q` and an upper-triangular or upper-trapezoidal factor `R`. This is a scope description, not the
canonical mathematical statement or a Lean target.

Axler Theorem 7.58 supplies one precise square, full-rank formulation. The statement phase must
either adopt that proposition after source acceptance or admit a source for a different rectangular
or rank-deficient formulation and record its relationship to the catalog wording.

## Decisions required at statement freeze

1. Choose `Real`, `Complex`, both via `RCLike`, or another explicitly sourced scalar domain.
2. Choose square matrices or rectangular `m`-by-`n` matrices, and fix finite index types and their
   orders. Upper triangularity depends on that order.
3. State any dimension relationship such as `m >= n` and any full-column-rank or invertibility
   hypothesis.
4. Choose full QR (square `Q`) or reduced/thin QR (column-orthonormal `Q`) and fix all factor shapes.
5. Define orthogonal/unitary orientation: `Q^T Q = I`, `Q^* Q = I`, membership in a group, or an
   equivalent basis/isometry representation.
6. Define upper triangular or upper trapezoidal `R`, including how a rectangular matrix is indexed.
7. Decide whether positive real diagonal entries, nonnegative diagonal entries, or complex phase
   normalization are required and whether uniqueness is part of the root.
8. Freeze the equality orientation, ordered binders, hypotheses, conclusion, universes, profiles,
   minimal imports, and every credited alternate encoding with checked transport.

These choices can change both truth conditions and proof obligations. Intake does not silently
resolve them from mathematical folklore.

## Boundary cases

The statement review must explicitly decide zero rows or columns, the `0`-by-`0` and `1`-by-`1`
cases, wide and tall matrices, the zero matrix, rank-deficient matrices, zero columns, repeated or
dependent columns, invertible square matrices, diagonal and already-triangular matrices, and real
matrices viewed inside the complex formulation. Positive-diagonal uniqueness generally interacts
with full column rank; it must not be attached to the rank-deficient family without proof and a
source.

## Excluded substitutions

- Gram-Schmidt orthogonalization, span preservation, or construction of an orthonormal basis alone
  is an ingredient, not the matrix equality with correctly shaped factors.
- Schur triangularization changes basis on both sides and is not QR factorization.
- LU, Cholesky, polar, singular-value, Jordan, and eigendecompositions are distinct theorems.
- A result restricted to invertible, square, full-rank, real, complex, or fixed-size matrices cannot
  close a broader root unless that restriction is part of the accepted exact statement.
- Approximate floating-point factors, numerical residuals, an algorithm run, or convergence of the
  QR eigenvalue algorithm do not prove exact existence.
- A structure or hypothesis storing `Q`, `R`, their properties, and `A = Q * R` supplies no proof.
- The catalog's `已验证` label, a theorem name, or successful `#check` supplies no H or M credit.

## Neighbor and duplicate boundaries

`THM-M-0045` owns Schur decomposition, `THM-M-0047` LU decomposition, and `THM-M-1448` is a
separate QR catalog target in the numerical-analysis category. The likely overlap with
`THM-M-1448` requires a later master identity decision; scope, artifacts, and status are not shared
between the two IDs. `THM-M-1451` owns the iterative QR eigenvalue algorithm, not factorization.

## Downstream handoff

The statement phase must admit and independently review an immutable pinpoint source; freeze field,
shape, order, rank, full/reduced, factor, triangularity, normalization, uniqueness, and boundary
conventions; elaborate a minimal-import Lean expression; preserve expression and environment
fingerprints; check transports; and run the required mutations. Only later phases may perform the
immutable anchor audit, freeze obligations and typed graphs, implement proof bodies, or claim
kernel closure.
