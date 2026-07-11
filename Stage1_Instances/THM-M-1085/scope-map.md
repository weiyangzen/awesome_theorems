# Scope map

## Included claim

- Two centered, finite-dimensional real Gaussian vectors indexed by the same finite nonempty set.
- Equality of corresponding coordinate variances.
- Pairwise comparison `Cov(X_i, X_j) <= Cov(Y_i, Y_j)` for distinct indices.
- For every real threshold `u`, the lower-tail comparison
  `P(max_i X_i <= u) <= P(max_i Y_i <= u)`.
- Degenerate Gaussian vectors and singular covariance matrices are intended to remain in scope if
  the selected exact source supports them.

This orientation passes the two-coordinate sanity check: decreasing covariance increases the
spread between coordinates and therefore increases the maximum, so its lower-tail probability
decreases.

## Statement-phase decisions

The selected primary statement must settle whether strict or non-strict threshold events are used,
whether the covariance comparison includes diagonal pairs, and whether degeneracy follows directly
or by approximation. The formal encoding must choose between random variables on one probability
space, separate laws, or multivariate Gaussian measures; define joint Gaussianity and covariance;
and fix measurability and finite-maximum APIs. Binder order, universes, imports, options, toolchain,
foundation profile, expression fingerprint, and checked alternate transports are all still open.

## Explicit exclusions

- The expectation-only comparison `E[max X_i] >= E[max Y_i]` as a substitute for the full
  threshold-by-threshold distribution inequality.
- A comparison of only one coordinate, independent coordinates only, or identically distributed
  coordinates only.
- Sudakov-Fernique's expectation inequality under increment-variance ordering.
- Gordon's min-max inequality, Gaussian correlation inequalities, or concentration bounds.
- An infinite or nonseparable Gaussian process without the extra approximation and regularity
  hypotheses needed to pass from finite maxima.
- Assuming the desired comparison as a field of an abstract structure.

The exclusions prevent a nearby Gaussian comparison theorem from silently replacing the named
claim. Any alternative formulation must receive a source-checked and kernel-checked transport in a
later phase.
