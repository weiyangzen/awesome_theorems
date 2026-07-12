# Scope map

## Included working boundary

- A separable infinite-dimensional complex Hilbert space, conventionally `l2(N)`.
- The C-star algebra of bounded operators on that space.
- The diagonal maximal abelian self-adjoint subalgebra determined by the standard basis.
- States on both algebras, purity of a state on the diagonal algebra, restriction, extension, and
  uniqueness.
- The affirmative solution of the 1959 Kadison-Singer question, once its exact source statement is
  frozen.

## Decisions required at statement freeze

The repository gloss does not decide whether to use concrete `l2(N)` or an abstract Hilbert space
with a chosen orthonormal basis. It also does not define a state (positive normalized linear
functional), pure state (extreme point versus order decomposition), the diagonal subalgebra, or
the restriction map. The exact source must determine whether the conclusion is uniqueness among
all state extensions, uniqueness among pure extensions, or existence and uniqueness together.

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

No canonical Lean target is frozen at intake.
