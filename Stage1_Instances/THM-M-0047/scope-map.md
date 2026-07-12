# THM-M-0047 scope map

## Preserved catalog boundary

The intake preserves the literal catalog family: a matrix is a product `L * U`, with `L` lower
triangular and `U` upper triangular. It does not yet freeze a canonical proposition because the
catalog omits the domain and conditions needed to make an LU theorem true.

## Literal-claim obstruction

Let `A = [[0, 1], [1, 0]]` over `Q`. For lower-triangular
`L = [[a, 0], [b, c]]` and upper-triangular `U = [[d, e], [0, f]]`, equality `A = L * U` gives
`a*d = 0`, `a*e = 1`, and `b*d = 1`. The latter two equations force both `a` and `d` nonzero,
contradicting `a*d = 0`. Thus even an invertible `2 x 2` matrix need not have an unpivoted LU
factorization. `IntakeProbe.lean` checks this argument over `Rat` in the pinned Lean environment.

## Decisions required before statement freeze

1. Whether the root is unpivoted LU with explicit pivot hypotheses, or pivoted PLU/LUP for a
   broader matrix class.
2. If a permutation occurs, whether the equation is `P * A = L * U`, `A = P * L * U`, another
   orientation, or a row-equivalence formulation.
3. Whether matrices are square or rectangular, and whether indices are `Fin n` or ordered finite
   types with a source-selected row/column ordering.
4. Whether scalars form a field, division ring, commutative ring, or another source-defined class.
5. Whether the input is arbitrary, invertible, rank-deficient, or subject to nonzero leading
   principal minors, nonzero pivots, or rank-profile conditions.
6. Whether `L` or `U` has unit diagonal and whether uniqueness is asserted under that
   normalization.
7. The exact triangular predicates, ordered binders, universes, hypotheses, conclusion, and all
   checked transports between matrix, elimination, and linear-map encodings.

These alternatives are not representation trivia. They select materially different theorems.

## Boundary and degenerate cases

Source review must decide the `0 x 0` and `1 x 1` cases, the zero matrix, singular matrices, zero
pivots, matrices needing row swaps, repeated or nonunique pivots, rectangular/tall/wide matrices,
and behavior over rings with zero divisors. It must also decide whether a permutation witness is
data, a permutation matrix, or an equivalence of index types.

## Excluded substitutions

- A pivoted PLU/LUP theorem cannot silently replace the literal unpivoted `A = L * U` gloss.
- A theorem assuming all leading principal minors are nonzero cannot silently replace a claim
  about arbitrary matrices.
- Gaussian elimination, row-echelon form, transvection-diagonal-transvection factorization, Schur
  decomposition, QR decomposition, Cholesky decomposition, or determinant multiplicativity is not
  the requested LU root.
- An algorithm, floating-point residual, numerical experiment, or factorization stored as an input
  structure is not an existence proof.
- The catalog's `已验证` label and a successful `#check` give no human-source or machine-proof credit.

## Neighbor and duplicate boundaries

`THM-M-0045` owns Schur decomposition, `THM-M-0046` QR decomposition, and `THM-M-0048` the
Cauchy-Binet formula. `THM-M-1446` is a separate numerical-analysis catalog record named `LU分解`
with the gloss "triangular decomposition of a matrix." It may be a duplicate lead, but its future
scope, evidence, and status cannot be inherited by this target without a master identity decision.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Matrix.BlockTriangular id` expresses upper triangularity and
`Matrix.BlockTriangular OrderDual.toDual` expresses lower triangularity. Matrix multiplication,
triangular determinant lemmas, and transvection/pivot reduction infrastructure are present. A
bounded local search found no declaration for LU, PLU, or LUP decomposition. These are intake
findings only, not the downstream exhaustive anchor audit or proof of global absence.
