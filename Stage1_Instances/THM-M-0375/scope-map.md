# Scope map

## Included topic boundary

- A Fourier transform on a source space fixed by an exact source.
- Restriction to a specified surface or hypersurface with a specified surface measure.
- A source-specified boundedness or norm estimate, including the exact exponent range, endpoints,
  dimension assumptions, normalization, and dependence of constants.
- The dual extension formulation only after a checked equivalence or both implications are supplied.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different claims:

1. The Stein-Tomas restriction estimate for the Euclidean unit sphere.
2. A Tomas-Stein extension estimate, dual to a restriction estimate only after all pairings,
   measures, exponent conjugacies, density steps, and normalizations are fixed.
3. A theorem for another curved hypersurface, with its own curvature and smoothness assumptions.
4. The general Fourier restriction conjecture or one of its known exponent/dimension cases.

The statement phase must identify an immutable source passage and freeze the ambient dimension,
surface, induced measure, transform convention, function class, `Lp` representation, exponent
interval and endpoints, and the exact uniformity of the constant. It must distinguish a pointwise
restriction from an almost-everywhere class and a bounded extension of an initially Schwartz-class
operator.

## Explicit exclusions

- Fourier inversion, Plancherel, Hausdorff-Young, or continuity of an `L1` Fourier transform as a
  substitute for a surface restriction estimate.
- The full Fourier restriction conjecture when the selected source proves only Stein-Tomas range.
- A sphere-only theorem if the source intends a broader class of hypersurfaces, or conversely.
- A tautological theorem that assumes the desired norm bound or bounded operator as input.
- Informal identification of restriction and extension formulations without a checked bridge.
- The repository label `verified` as evidence of either a human proof or kernel closure.

No canonical Lean target is frozen at intake because the source record does not identify one.

