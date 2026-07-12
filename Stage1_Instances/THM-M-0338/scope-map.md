# Scope map

## Included working boundary

- A separable infinite-dimensional complex Hilbert space, conventionally `l2(N)`.
- The C-star algebra of bounded operators on that space.
- The diagonal maximal abelian self-adjoint subalgebra determined by the standard basis.
- States on both algebras, purity of a state on the diagonal algebra, restriction, extension, and
  uniqueness.
- The affirmative solution of the 1959 Kadison-Singer question, once its exact source statement is
  frozen.

## Statement decisions

The frozen statement uses an abstract complete complex inner-product space with a `Nat`-indexed
Hilbert basis. A state is a positive complex-linear functional normalized at one, purity is the
extreme-point condition, and the diagonal star subalgebra is characterized by vanishing
off-diagonal matrix coefficients. The conclusion is existence and uniqueness among all state
extensions, with restriction expressed through the subalgebra coercion.

Boundary cases needing explicit treatment include finite-dimensional spaces, an empty or finite
index type, nonseparable spaces, nonunital algebras, and a subalgebra that is merely commutative or
maximal abelian rather than the distinguished diagonal algebra.

## Explicit exclusions

- The paving conjecture, Weaver discrepancy conjectures, restricted invertibility, or mixed
  characteristic polynomials as substitutes. They may later be source-crosswalked equivalent
  formulations, but are not the repository's literal claim.
- A generic Hahn-Banach extension theorem, which supplies neither purity nor uniqueness.
- Unique extension from an arbitrary maximal abelian subalgebra.
- A finite-dimensional analogue, where the deep infinite-dimensional content disappears.
- Treating `PositiveLinearMap` alone as a state without normalization and purity predicates.
- Treating the repository label `已验证` as human-proof or kernel-proof evidence.

The canonical Lean target is frozen in `Statement.lean`; these exclusions remain statement
boundaries and do not assert the target is proved.
