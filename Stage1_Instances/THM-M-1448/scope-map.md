# THM-M-1448 scope map

## Preserved theorem family

The intake preserves the finite real-or-complex QR factorization family indicated by the catalog:
a matrix factors exactly as `A = Q * R`, with an orthogonal/unitary or column-orthonormal factor
`Q` and an upper-triangular or upper-trapezoidal factor `R`. This is a scope description, not the
canonical mathematical statement or a Lean target.

Axler Theorem 7.58 supplies one precise square, full-column-rank formulation. The statement phase
must either adopt that proposition after source acceptance or admit a source for a different
rectangular or rank-deficient formulation and record its relationship to the catalog wording.

## Decisions required at statement freeze

1. Choose `Real`, `Complex`, both through an `RCLike` generalization, or another explicitly sourced
   scalar domain.
2. Choose square matrices or rectangular `m`-by-`n` matrices, and fix finite index types and their
   orders. Upper triangularity depends on the order.
3. State any dimension relation such as `m >= n` and any full-column-rank, nonzero-column, or
   invertibility hypothesis.
4. Choose full QR (square `Q`) or reduced/thin QR (column-orthonormal `Q`) and fix all factor shapes.
5. Define orthogonal/unitary orientation: `Q^T Q = I`, `Q^* Q = I`, group membership, or a checked
   equivalent basis/isometry representation.
6. Define upper triangular or upper trapezoidal `R`, including the rectangular index convention.
7. Decide whether positive or nonnegative diagonal entries, or complex phase normalization, are
   required and whether uniqueness belongs to the root.
8. Freeze equality orientation, ordered binders, hypotheses, conclusion, universes, profiles,
   minimal imports, and every credited alternate encoding with a checked transport.

These choices change truth conditions or proof obligations. Intake does not silently resolve them
from mathematical folklore or from the catalog's untrusted status label.

## Boundary cases

Source review must decide zero rows or columns, the `0`-by-`0` and `1`-by-`1` cases, wide and tall
matrices, the zero matrix, rank-deficient matrices, zero or dependent columns, invertible square
matrices, diagonal and already-triangular matrices, and real matrices viewed inside a complex
formulation. Positive-diagonal uniqueness interacts with full column rank and must not be attached
to a rank-deficient family without a matching source and proof.

## Excluded substitutions

- Gram-Schmidt orthogonalization, span preservation, or orthonormal-basis construction alone is an
  ingredient, not the matrix equality with correctly shaped factors.
- Schur triangularization changes basis on both sides and is not QR multiplication.
- LU, Cholesky, polar, singular-value, Jordan, and eigendecompositions are distinct theorems.
- A square, invertible, full-rank, real-only, complex-only, or fixed-size result cannot close a
  broader root unless that restriction is part of the accepted statement.
- Approximate floating-point factors, residuals, a numerical routine, or convergence of the QR
  eigenvalue algorithm do not prove exact existence.
- A structure or hypothesis storing `Q`, `R`, their properties, and `A = Q * R` supplies no proof.
- The catalog's `已验证` label, a theorem-name match, or a successful `#check` supplies no H or M
  credit.

## Neighbor and duplicate boundaries

`THM-M-0046` is a likely duplicate QR catalog entry in the linear-algebra category, but its scope,
artifacts, receipts, and status are not inherited. `THM-M-1447` owns Cholesky decomposition,
`THM-M-1449` singular-value decomposition, and `THM-M-1451` the iterative QR eigenvalue algorithm.
None substitutes for this factorization target. A master identity decision may later relate the two
QR IDs; intake records the overlap without broadening either target.

## Formal boundary and handoff

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe
checks Gram-Schmidt, orthonormal-basis, unitary-matrix, and block-triangular APIs. It does not define
a canonical target. The statement phase must admit and independently review a pinpoint source;
freeze field, shape, order, rank, full/reduced, factor, triangularity, normalization, uniqueness,
and boundary conventions; elaborate a minimal-import Lean expression; preserve expression and
environment fingerprints; check transports; and run required mutations. Only later phases may
perform the exhaustive anchor audit, freeze obligations and typed graphs, implement proof bodies,
or claim kernel closure.
