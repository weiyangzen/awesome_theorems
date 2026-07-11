# Scope map

## Included claim

- A sequence of independent, identically distributed real random variables on a probability
  space, with expectation zero and finite variance `sigma^2`, where `sigma > 0`.
- Partial sums starting at zero, normalized by `sigma * sqrt(n)`.
- The continuous polygonal interpolation through the normalized values at times `k/n`, including
  the endpoint at time one.
- Weak convergence of the induced laws on `C([0,1], R)` with its uniform topology to Wiener
  measure, equivalently convergence in distribution to standard real Brownian motion as a
  continuous-path random variable.

This is the classical finite-variance i.i.d. functional central limit theorem. The formulation with
variance one is admissible only through a checked normalization transport, not by silently deleting
`sigma` from the claim.

## Statement-phase decisions

The statement phase must choose and elaborate one exact encoding of:

- the common probability space and i.i.d. predicate, integrability and square-integrability;
- the natural-number indexing convention (`X 0` versus `X 1`) and empty partial sum;
- positive variance versus a standardized variance-one hypothesis;
- polygonal interpolation, including `n = 0`, floor/index bounds, and the final subinterval;
- continuous maps on `Set.Icc (0 : R) 1` versus an equivalent unit-interval type;
- convergence in distribution as weak convergence of pushforward laws, including measurability;
- standard Brownian motion/Wiener measure and the uniform-topology Borel structure.

Binder order, universes, imports, foundation/TCB profiles, and the canonical expression fingerprint
remain open until those choices elaborate under the pinned Lean environment.

## Boundary cases requiring explicit treatment

- `sigma = 0` is excluded by the positive-variance hypothesis; a degenerate constant walk is not
  the standard-Brownian conclusion.
- The interpolation formula must be total at `t = 1` and must not index beyond the `n`th increment.
- No conclusion is claimed for infinite variance or nonzero drift without a separately checked
  centering/scaling transport.

## Explicit exclusions

- A scalar central limit theorem only at time one.
- Finite-dimensional distribution convergence without tightness/path-space weak convergence.
- A step-function process in Skorokhod `D([0,1])` unless equivalence to the selected continuous
  interpolation statement is formally transported in the required direction.
- Triangular arrays, dependent or merely stationary sequences, multidimensional increments,
  stable-law limits, strong invariance principles, or quantitative convergence rates.
- Assuming that the rescaled walk already converges to Brownian motion, or wrapping an abstract
  invariance-principle hypothesis whose conclusion is the target.

The later formal target must connect actual increments, partial sums, interpolation, induced laws,
the path topology, and an actual Brownian/Wiener limit, or record a precise missing-API blocker.
