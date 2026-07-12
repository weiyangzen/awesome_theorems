# Scope map

## Included topic boundary

- Analytic sets in descriptive set theory, not analytic subsets from complex or real analysis.
- The source-specified ambient Polish, Hausdorff, or standard Borel space.
- Analyticity of a set and its complement (coanalyticity), with the exact coding convention.
- The precise Borel or measurable conclusion and all topology/measurable-space compatibility
  assumptions.

## Ambiguities to resolve at statement freeze

The repository phrase "the complement property of analytic sets" is compatible with materially
different claims:

1. If `s` and `sᶜ` are analytic, then `s` is Borel (the usual hard direction of Suslin's theorem).
2. A set is Borel if and only if it and its complement are analytic, incorporating the converse.
3. Borel sets are analytic and have analytic complements, a weaker closure consequence.
4. Analytic sets are not in general closed under complements, an existence/non-closure theorem.

The statement phase must inspect an immutable source and freeze one proposition. It must specify
the ambient space, separation and countability assumptions, the definition of analytic set,
whether "Borel" is expressed as membership in `borel` or as `MeasurableSet` under an
`OpensMeasurableSpace`, and the ordered binders, hypotheses, and conclusion.

## Explicit exclusions

- Analytic functions or analytic subsets in complex/real-analytic geometry.
- Lusin separation alone as a substitute, although it may be a proof dependency.
- Closure of analytic sets under continuous images, countable unions, or intersections.
- A tautology obtained by assuming the desired measurability or Borel conclusion.
- The pinned mathlib candidate as proof that it is identical to the unspecified source claim.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not uniquely identify
the theorem's formulation.
