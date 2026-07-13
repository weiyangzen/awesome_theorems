# THM-M-1446 scope map

## Preserved catalog boundary

The intake preserves exactly the catalog topic `矩阵的三角分解` under the title `LU分解`. That text
does not specify a binder-complete claim, so this phase does not silently promote a familiar LU,
LDU, PLU, or LUP variant to the canonical theorem.

## Literal-claim obstruction

Let `A = [[0, 1], [1, 0]]` over the rationals. If
`L = [[a, 0], [b, c]]` is lower triangular and `U = [[d, e], [0, f]]` is upper triangular, then
`A = L * U` implies `a*d = 0`, `a*e = 1`, and `b*d = 1`. The latter two equations force `a` and
`d` nonzero, contradicting the first. Thus even an invertible square matrix need not possess an
unpivoted LU factorization. `IntakeProbe.lean` checks this exact boundary over `Rat`.

## Decisions required before statement freeze

1. Whether the root is Turing's qualified LDU theorem, a qualified unpivoted LU theorem, or a
   pivoted PLU/LUP theorem.
2. Whether a permutation appears and, if so, whether the equation is `P * A = L * U`,
   `A = P * L * U`, `P * A * Q = L * U`, or another orientation.
3. Whether matrices are square or rectangular and how ordered row and column indices are encoded.
4. Whether scalars form a field, division ring, commutative ring, or another source-defined class.
5. Whether the input is arbitrary, invertible, full rank, or subject to nonsingular leading
   principal minors, nonzero pivots, or rank-profile conditions.
6. Whether a diagonal factor is explicit, which triangular factor has unit diagonal, and whether
   existence alone or normalized uniqueness is asserted.
7. Whether Turing's reverse `U' * D' * L'` clause belongs to the root.
8. The ordered binders, hypotheses, conclusion, alternate encodings, checked transports, and every
   boundary convention.

These choices identify different theorems rather than harmless presentational variants.

## Boundary and degenerate cases

Source review must decide zero- and one-dimensional matrices; zero, singular, and invertible
matrices; zero pivots and matrices requiring swaps; rectangular or rank-deficient matrices;
nonunique factors; rings with zero divisors; the meaning of "principal minors"; and whether a
permutation is a matrix, index equivalence, or elimination witness.

## Excluded substitutions

- A pivoted theorem cannot silently replace an unpivoted theorem.
- Turing's nonsingular-principal-minor hypothesis cannot be dropped, and it cannot be inserted into
  the catalog gloss without a reviewed source decision.
- Gaussian elimination, row-echelon form, transvection-diagonal-transvection factorization, Schur,
  QR, Cholesky, determinant identities, or numerical residual bounds are not this root.
- A fixed example, algorithm, floating-point experiment, or structure already storing factors is
  not a general factor-existence proof.
- The catalog's `已验证` label, the checked counterexample, and an API `#check` supply no corrected-root
  source or machine-proof credit.

## Neighbor and duplicate boundaries

`THM-M-1445` owns Gaussian elimination, `THM-M-1447` Cholesky decomposition, and `THM-M-1448` QR
decomposition. `THM-M-0047` is a separate algebra/linear-algebra catalog record called `LU分解定理`
with a more explicit lower-times-upper gloss. It is a strong duplicate lead, but target identity,
scope, evidence, receipts, and state remain separate unless the master records an identity decision.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Matrix.BlockTriangular id` expresses upper triangularity and
`Matrix.BlockTriangular OrderDual.toDual` lower triangularity. Matrix multiplication, determinant
lemmas, and pivot/transvection infrastructure are available. A bounded intake search found only
specialized block LDU identities in `Matrix.SchurComplement`, not a general exact LU/PLU/LUP/LDU
terminal declaration. This is a discovery note, not the downstream exhaustive anchor audit.
