# THM-M-1455 scope map

## Preserved theorem family

The intake preserves the exact-arithmetic conjugate-gradient method for finite-dimensional
symmetric positive-definite linear systems as the named family. A later statement phase may select
a canonical root only after an immutable primary-source passage and all incorporated definitions
are mapped and independently reviewed. Candidate components, none credited as the theorem, are:

- a real symmetric positive-definite matrix `A`, right-hand side `b`, solution `h`, and initial
  estimate `x0`;
- residuals `r_i = b - A x_i`, search directions `p_i`, and the source-defined `alpha` and `beta`
  recurrence;
- pairwise orthogonality of residuals and `A`-conjugacy of search directions;
- membership of iterates and directions in the appropriate Krylov spaces;
- minimization of the quadratic error functional or `A`-norm over an affine Krylov space;
- strict error decrease before termination; and
- exact termination in at most the finite dimension when no rounding error occurs.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source rather than from a
generic numerical-linear-algebra convention:

1. The exact edition, result locator, incorporated definitions, proof boundary, correction history,
   and independent source review.
2. Whether the root is recurrence correctness, Theorem 5:1 orthogonality/conjugacy, Theorem 5:2's
   conjugate-direction characterization, Theorem 6:1 minimization/decrease, finite termination, a
   convergence bound, or a checked conjunction.
3. The real or complex scalar field, finite index and dimension, matrix or operator representation,
   inner product, norm, symmetry/Hermitian convention, and positive-definiteness predicate.
4. The exact binders for `A`, `b`, `x0`, iterates, residuals, directions, coefficients, iteration
   count, solution, and any eigenvalue or condition-number parameters.
5. The recurrence convention and whether nonzero denominators are derived from positive
   definiteness, assumed, or represented by an early-termination branch.
6. Whether arithmetic is exact or floating-point. The 1952 finite-termination result is expressly
   conditional on no rounding error and does not prove stability of an executable solver.
7. The exact conclusion and logic strength, including whether existence, uniqueness, convergence,
   complexity, storage, restarting, or preconditioning is in scope.

## Degenerate and boundary cases

Source review must explicitly dispose of dimension zero and one; `b = 0`; `x0` already solving the
system; `r0 = 0`; an identity or scalar matrix; repeated eigenvalues; early Krylov-space
stabilization; zero numerator or denominator in a recurrence; an iteration count at or beyond the
dimension; and the distinction among exact termination, convergence, residual behavior, error
decrease, rounding error, restart, and preconditioning.

## Explicit exclusions

- `THM-M-1503` nonlinear or optimization conjugate gradient is a separate target; it cannot replace
  the requested linear-system method.
- GMRES (`THM-M-1454`), Lanczos (`THM-M-1452`), Arnoldi (`THM-M-1453`), MINRES, steepest descent,
  or a generic conjugate-directions theorem alone is not this target.
- Positive-definite invertibility or existence of the exact solution alone does not establish the
  conjugate-gradient recurrence, its invariants, or its output.
- A theorem assuming residual orthogonality, direction conjugacy, minimization, convergence, or
  finite termination as stored data cannot supply the missing proof.
- A scalar or fixed-size example, numerical trajectory, tolerance test, floating-point benchmark,
  residual plot, or executable solver run is not an exact theorem proof.
- A preconditioned, restarted, flexible, block, stochastic, or finite-precision variant is not
  silently interchangeable with the source method.
- Generic matrix-vector, positive-definiteness, dot-product, spectral, or Krylov infrastructure
  supplies no root theorem credit.
- The repository label `已验证` supplies no human-source or machine-proof evidence.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen at intake.
