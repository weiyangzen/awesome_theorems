# Scope map

## Included claim

- Finite-dimensional real Euclidean space with its standard Gaussian probability measure.
- A measurable set `A` and its metric `r`-enlargement for nonnegative `r`.
- Comparison with a half-space having the same Gaussian measure.
- Equivalently, after conventions are frozen, a lower bound of the form
  `gamma (A_r) >= Phi (PhiInv (gamma A) + r)`.

## Decisions reserved for the statement phase

An inspected source must fix whether enlargement uses `< r` or `<= r`, the treatment of `r = 0`,
null/full-measure sets and extended quantiles, whether the statement is for every positive
dimension, and whether measurability of the enlargement needs an explicit hypothesis or follows
from the selected finite-dimensional model. It must also fix normalization of Gaussian measure,
Euclidean distance, `Phi`, and its inverse before Lean binders and universes are frozen.

## Explicit exclusions

- Substituting a one-dimensional Gaussian tail estimate, Chernoff bound, or concentration result
  only for Lipschitz functions.
- Replacing Gaussian measure by an arbitrary sub-Gaussian distribution or an infinite-dimensional
  abstract Wiener space.
- Proving only that half-spaces attain a formula without the extremal comparison for all sets.
- Treating the manifest's untrusted `已验证` label or a library-adjacent fact as proof credit.

The formal target must expose concrete Gaussian measure, metric enlargement, and normal CDF
interfaces. Missing mathlib API is an integration obligation, not permission to broaden the claim.
