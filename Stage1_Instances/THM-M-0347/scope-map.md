# Scope map

## Included claim

- A continuous periodic function, represented on a circle rather than as an arbitrary function on
  the real line with an implicit periodicity convention.
- Its Fourier coefficients and symmetric Fourier partial sums under one frozen normalization.
- First-order Cesaro means (arithmetic means) of those partial sums.
- Uniform convergence of the means to the original function; pointwise convergence may be exposed
  only as a checked consequence.
- The constant-function and initial-index boundary cases under the chosen convention.

## Boundary decisions for the statement phase

The exact source must fix or justify the circle period, normalized versus unnormalized Haar
measure, the sign and scale in the Fourier characters, complex versus real codomain, and the
symmetric partial sum range. It must also decide whether the `n`th mean averages partial sums
`S_0, ..., S_n` or `S_0, ..., S_(n-1)`, how the zero denominator is avoided, and whether convergence
is phrased in the continuous-map sup norm or by a uniform-convergence predicate.

The duplicate repository target `THM-M-0291` has the stronger gloss "uniform convergence". It is
discovery context only: targets must not be merged, and no proof or source credit transfers between
them. For this harmonic-analysis entry, the standard uniform Fejer theorem is the intended family,
but the statement phase must confirm that reading from an immutable source rather than silently
strengthen the shorter gloss.

## Explicit exclusions

- Ordinary convergence of the raw Fourier partial sums of every continuous function.
- Dirichlet's theorem under differentiability or bounded-variation hypotheses as a substitute.
- Pointwise or norm convergence for merely integrable functions as a substitute for the continuous
  uniform theorem.
- The Riesz-Fejer theorem, Poisson summation, Carleson's theorem, or an ergodic Cesaro theorem.
- An abstract package taking the desired convergence as an assumption.
- The manifest label `已验证`, an API probe, or a theorem about absolutely summable Fourier
  coefficients as proof of Fejer's theorem.

No canonical Lean expression or alternate-encoding transport is credited at intake.
