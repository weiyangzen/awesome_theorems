# Scope map

## Candidate included claim

- A stochastic differential equation with small noise, provisionally of the form
  `dX^epsilon_t = b(X^epsilon_t) dt + sqrt(epsilon) sigma(X^epsilon_t) dW_t` on a fixed finite
  time interval.
- A large-deviation lower bound for open path sets and upper bound for closed path sets.
- A good action rate function defined by controlled trajectories (or the source-equivalent
  inverse-covariance formula where justified).
- The path space, topology, initial condition, coefficient regularity, degeneracy assumptions, and
  speed exactly as fixed by the selected primary theorem.

This is a candidate interpretation, not a frozen exact claim. "Freidlin-Wentzell theory" also
includes exit-time and invariant-measure asymptotics; the repository's phrase does not select among
them. The statement phase must select one source theorem without silently combining several.

## Required boundary decisions

Primary-source inspection must fix finite- versus infinite-dimensional state space, additive versus
multiplicative and degenerate versus nondegenerate noise, the initial-condition quantifiers, uniform
versus pointwise LDP, path topology, the normalization of noise and LDP speed, and whether the rate
is expressed through controls or an inverse diffusion matrix. It must also fix the meaning at paths
without an admissible control and all compactness/exponential-tightness hypotheses.

## Explicit exclusions

- A generic abstract LDP assumed as a hypothesis or stored as structure data.
- Varadhan's lemma, Schilder's theorem, or the contraction principle alone.
- Convergence in probability to the deterministic ODE without exponential bounds.
- Exit-location, quasipotential, metastability, or invariant-measure results substituted for the
  selected path-space theorem.
- A finite-state toy model presented as the unrestricted classical diffusion theorem.

The formal target must expose the probability laws, scaling, topology, rate function, and both LDP
bounds; naming a prepackaged proposition without auditing those fields is insufficient.
