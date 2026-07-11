# Scope map

## Included claim

- A complex Hilbert space and a normalized vector state.
- Two self-adjoint observables, with explicit common-domain hypotheses sufficient to define the
  expectations, variances, and both operator products in the commutator.
- The Robertson bound `Delta(A) * Delta(B) >= |<psi, [A,B] psi>| / 2`.
- The position-momentum corollary under `[Q,P] = i * hbar * I` and `0 <= hbar`.

## Boundary decisions for the statement phase

The selected primary source must determine whether the root is the general Robertson inequality,
the position-momentum inequality, or a checked conjunction/corollary relation. The statement phase
must freeze inner-product orientation, variance definition, square-root convention, self-adjoint
versus symmetric hypotheses, normalization, operator domains, the scope of the CCR, and degenerate
cases such as zero variance and `hbar = 0`. Universes and binder order must then be explicit.

## Explicit exclusions

- An informal measurement-disturbance slogan or experimental assertion.
- Fourier width inequalities with unspecified width as a substitute for operator variance.
- Finite matrices or bounded everywhere-defined maps presented as the full physical theorem without
  a proved transport or an explicit restricted-model label.
- A structure or hypothesis that assumes the desired uncertainty inequality.
- The legacy `S1_M_192.lean` result as rev-5.6 proof credit before exact-statement comparison.

The later formal target must model the unbounded-operator domain boundary faithfully or record a
precise representation blocker; silently replacing it by bounded operators would broaden the claim.
