# Scope map

## Included claim

- A probability space and a sequence of real-valued random variables.
- Identical distribution and mutual independence of the entire sequence.
- Finite second moment, hence a finite mean and variance, for a reference summand.
- Centering by `n` times the common expectation and normalization by `sqrt n`.
- Convergence in distribution to the centered real Gaussian law with the common variance.

## Statement-phase decisions

The exact source edition must settle whether variance is required positive or may be zero, and
whether the theorem states a standard-normal limit after division by the standard deviation or a
Gaussian with variance `variance X`. The Lean statement must freeze measurability/integrability
requirements, probability measures, index set, the `n = 0` convention, binder order, universes,
and the precise `TendstoInDistribution` encoding. Degenerate zero variance must not be silently
excluded or introduced.

## Explicit exclusions

- Lindeberg-Feller triangular arrays, Lyapunov's CLT, multivariate CLTs, or dependent sequences.
- Convergence only of characteristic functions, moments, or finite numerical experiments.
- A standard-normal conclusion without the required nonzero-variance hypothesis and scaling.
- Treating the legacy wrapper or an upstream theorem name as accepted rev-5.6 proof evidence.

The later exact target may use the pinned mathlib convergence-in-distribution API only after a
row-by-row equivalence check against the selected source statement.
