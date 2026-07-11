# Scope map

## Included claim

- A triangular array of real random variables, with independence within each finite row.
- Centering by each entry's expectation and scaling by the square root of the sum of row variances.
- A fixed real `delta > 0` and finite absolute centered moments of order `2 + delta`.
- The Lyapunov ratio tending to zero as the row index tends to infinity.
- Weak convergence in distribution of normalized row sums to the standard Gaussian law.

## Decisions reserved for statement phase

The inspected primary source must fix row length (`n` versus a separate `k_n`), whether variables
are initially assumed centered, positivity versus divergence of variance sums, the precise moment
integrability formulation, and whether the conclusion uses distribution functions or weak
convergence of laws. The Lean target must also fix probability-space variation across rows,
measurability, binder order, universes, and degenerate rows. These choices must not be inherited
silently from the legacy module.

## Explicit exclusions

- The identically distributed CLT, Lindeberg-Feller CLT, or Berry-Esseen bound as a substitute.
- Pairwise independence in place of the source theorem's joint row independence.
- A finite or discrete special case presented as the full theorem.
- Assuming characteristic-function convergence, a Taylor bridge, or the desired weak convergence
  as structure data.
- The wrappers and boundary metadata in `S1_M_270.lean` as terminal proof evidence.

The statement phase must produce a concrete mathlib expression and checked boundary cases; until
then the human scope is frozen but the formal target remains open.
