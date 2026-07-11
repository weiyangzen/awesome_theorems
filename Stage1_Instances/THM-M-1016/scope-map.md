# Scope map

## Included claim

- Random elements `X_n`, a centering point `theta`, positive scaling constants `r_n`, and a limit
  random element `Z` with `r_n (X_n - theta)` converging in distribution to `Z`.
- A transformation `g` differentiable at `theta` in the sense required by the selected source.
- The conclusion that `r_n (g(X_n) - g(theta))` converges in distribution to the derivative at
  `theta` applied to `Z`.

## Decisions deferred to statement freeze

The selected and inspected source must decide scalar versus finite-dimensional or normed-space
random elements, ordinary/Frechet/Hadamard differentiability, deterministic versus more general
scaling, whether `r_n` tends to infinity, Borel measurability and separability hypotheses, and the
precise definition of convergence in distribution. Binder order, universes, topology, probability
spaces, and degenerate cases such as zero derivative must follow that source.

## Explicit exclusions

- Replacing convergence in distribution by convergence in probability or almost sure convergence.
- Assuming the transformed convergence as a hypothesis or packaging it as structure data.
- The second-order delta method, delta method for estimators with estimated variance, or the
  functional delta method unless the chosen exact source is explicitly that variant.
- A normal-limit-only corollary substituted for a more general frozen source statement.

The statement phase must identify the concrete mathlib representation of random variables,
distributional convergence, continuous linear derivatives, scalar multiplication, and measurable
composition, or record an exact API blocker.
