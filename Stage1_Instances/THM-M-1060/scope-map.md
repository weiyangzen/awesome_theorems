# Scope map

## Included claim

- Standard real Brownian motion on a fixed finite interval `[0,T]`, represented by its law on
  based continuous path space `C_0([0,T], R)` with the uniform topology.
- The family of pushforward laws under path scaling `w -> sqrt(epsilon) * w`, for `epsilon > 0`
  tending to zero.
- The full large-deviation upper bound for closed sets and lower bound for open sets, at speed
  `1 / epsilon` (equivalently the corresponding normalization convention).
- The good Cameron-Martin rate function: half the squared `L2` norm of the derivative on
  absolutely continuous based paths, and `+infinity` outside that class.

## Statement-phase decisions

The selected source must fix `T` (or justify transport from `[0,1]`), the topology and Borel
structure, extended-real conventions, the exact LDP normalization, and whether exponential
tightness/goodness is part of the named theorem. The statement must also settle the zero horizon,
empty open/closed sets, measurability of path scaling, and the encoding of absolutely continuous
paths and a.e. derivatives. Binder order and universes must follow those decisions.

## Explicit exclusions

- A finite-dimensional Gaussian tail estimate or Cramer's theorem as a substitute for path-space
  large deviations.
- Only the upper bound, only the lower bound, or only compact subsets.
- Freidlin-Wentzell large deviations for general stochastic differential equations.
- Merely defining an abstract `LargeDeviationPrinciple` structure and assuming its fields.
- Replacing Brownian motion by an arbitrary process already assumed to satisfy the desired LDP.

The later formal target must connect an actual Wiener measure/Brownian law, path scaling, topology,
and Cameron-Martin energy, or record a precise missing-API blocker.
