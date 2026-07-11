# Scope map

## Included claim

- A continuous-time Markov diffusion `X` on a state space, with infinitesimal generator `L`.
- A backward parabolic terminal-value problem on a finite horizon with terminal payoff `g`.
- A killing potential `V`, additive source `f`, and the corresponding exponentially weighted
  expectation along `X`.
- Explicit hypotheses sufficient for the diffusion, path integral, expectation, classical PDE
  solution, and uniqueness statement once a primary theorem is selected.

## Boundary decisions for the statement phase

The selected source must freeze whether the state space is `R^d` or a more general domain; the SDE
coefficients and ellipticity assumptions; scalar codomain; boundedness, continuity, and derivative
requirements; stopping at a domain exit; and whether the theorem proves representation, existence,
uniqueness, or an equivalence. It must also freeze calendar-time versus time-to-maturity orientation
and all signs. Universes and binder order must follow that source rather than the legacy wrapper.

## Explicit exclusions

- A discrete-time dynamic-programming identity or finite-state specialization substituted for the
  continuous-time diffusion theorem.
- The heat equation alone, a path-integral heuristic, or a formula without its analytic and
  probabilistic hypotheses.
- An abstract structure that contains the desired probabilistic representation as a field.
- Kernel composition, deterministic-kernel integration, or convention projection lemmas treated as
  proof of Feynman-Kac.

The later statement must give concrete meanings to the process law, generator, exponential path
functional, PDE derivatives, boundary data, and integrability conditions, or record an exact API
blocker.
