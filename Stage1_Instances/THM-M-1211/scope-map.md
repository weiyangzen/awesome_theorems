# Scope map

## Included theorem family

- Space-time local smoothing estimates for the wave propagator or, if the selected source uses
  that generality, a Fourier integral operator satisfying the stated cinematic-curvature and
  nondegeneracy hypotheses.
- The precise comparison between a fixed-time Sobolev estimate and an integrated-in-time estimate,
  including the source's derivative gain or loss.
- Only the dimension, `L^p` range, compact time interval, frequency localization, and endpoint
  assertions belonging to the selected theorem.

## Decisions required before statement freeze

The statement phase must identify a stable primary source and exact theorem/page. It must fix the
operator and Fourier-transform conventions, spatial manifold/domain and dimension, scalar field,
time interval, cutoff/support assumptions, Sobolev or Bessel-potential norms, exponent range,
frequency parameter, derivative exponent, constants and their dependencies, and endpoint status.
It must distinguish a proved estimate from the broader local smoothing conjecture and state all
curvature hypotheses rather than hiding them in an assumed result structure.

## Explicit exclusions

- A fixed-time wave estimate substituted for a genuine space-time smoothing estimate.
- The local smoothing conjecture in an exponent range not proved by the selected source.
- A Euclidean special case substituted for a variable-coefficient theorem, or conversely.
- A decoupling theorem, maximal estimate, Strichartz estimate, or generic interpolation lemma
  presented as the named theorem without a checked equivalence.
- An abstract predicate that assumes the desired estimate as a field.

Degenerate frequencies, zero input, empty/zero-length time intervals, endpoint exponents, and the
meaning of fractional differentiation must be mapped explicitly in the eventual Lean statement.
