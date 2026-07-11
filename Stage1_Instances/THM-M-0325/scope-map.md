# Scope map

## Included claim

- Finite index sets and a real scalar matrix `A`.
- A scalar bilinear-form supremum over real scalars of absolute value at most one.
- A Hilbert-space form obtained by replacing scalar products with inner products of unit vectors.
- Existence of one nonnegative real constant independent of the matrix, index sets, Hilbert space,
  and scalar bound.
- The inequality in a formulation equivalent to the classical real finite-matrix theorem once the
  source normalization is verified.

## Decisions reserved for the statement phase

The inspected primary source must settle sign vectors versus the full unit polydisc, whether the
scalar bound is expressed as a supremum or as a universally quantified bound `C`, real versus
complex constants, finite-dimensional versus arbitrary real Hilbert spaces, and the convention for
empty index types and negative `C`. Binder universes and the exact positivity condition on the
constant must then be frozen in Lean and mutation-tested.

## Explicit exclusions

- The complex Grothendieck inequality as a substitute for the real theorem.
- A little Grothendieck theorem, Grothendieck's theorem on nuclear spaces, or a tensor-product
  slogan without a checked equivalence to the finite-matrix claim.
- Any dimension-dependent constant or restriction to one chosen Hilbert space.
- A structure or hypothesis that assumes the desired terminal inequality.
- The legacy `StatementShape` or its elementary substrate wrappers as proof of the theorem.

Tensor-norm and bounded-bilinear formulations may be registered later only with checked transports
to the selected source statement.
