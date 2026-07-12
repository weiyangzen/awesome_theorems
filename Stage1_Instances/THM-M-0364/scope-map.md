# Scope map

## Included theorem family

- David and Journe's 1984 boundedness criterion for generalized Calderon-Zygmund operators.
- The exact source-specified operator or bilinear-form domain and generalized Calderon-Zygmund
  kernel hypotheses.
- The source-specified weak boundedness property and the conditions on `T(1)` and `T*(1)`.
- The exact BMO convention, adjoint interpretation, and conclusion giving an L2-bounded extension.
- Every dimension, scalar, regularity, support, normalization, and measure assumption required by
  the selected primary-source theorem.

## Decisions required at statement freeze

The repository gloss does not determine whether the canonical claim is an equivalence or only the
sufficiency direction, nor does it specify the generalized singular-integral setup. The statement
phase must freeze:

1. the underlying space and measure, dimension, scalar field, test-function class, and operator or
   bilinear-form representation;
2. kernel size and smoothness estimates, constants, and the meaning of agreement off the diagonal;
3. the exact weak boundedness property and its normalization;
4. how `T(1)` and `T*(1)` are defined when the constant function is not in the initial domain, and
   the precise BMO space/modulo-constants convention;
5. the adjoint and duality pairings, and whether real or complex conjugation is involved;
6. whether the conclusion asserts a unique continuous extension to L2, a norm estimate, or an
   if-and-only-if criterion.

## Explicit exclusions

- The slogan "a singular integral operator is L2 bounded" without the T(1) hypotheses.
- The classical convolution Calderon-Zygmund theorem, Hilbert-transform boundedness, a `Tb`
  theorem, or a dyadic/probabilistic T(1) theorem as a substitute.
- Any finite-dimensional bounded-linear-map tautology or an assumption of continuity used to prove
  the desired continuity.
- A theorem only about `MemLp`, integrability, or a generic continuous linear map.
- The repository label `verified` as evidence of source fidelity or machine closure.

No canonical Lean proposition is frozen at intake. The API probe merely establishes that some
generic measure/Lp/operator ingredients exist in the pinned environment.
