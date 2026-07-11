# Scope map

## Included claim

- A Polish space `X`: a separable, completely metrizable topological space, with its Borel
  measurable structure.
- A set `S` of Borel probability measures on `X`.
- Uniform tightness: for every positive error there is one compact subset of `X` outside which
  every measure in `S` has mass below that error.
- Relative compactness of `S` for weak convergence of probability measures.
- Both implications of the equivalence, including empty and finite families.

## Decisions deferred to statement work

The selected primary source must fix whether relative compactness means compact closure or
sequential relative compactness, the exact strict/non-strict error inequality, and whether the
space is presented as Polish or by explicit complete metric and second-countability instances.
The statement phase must also reconcile `ProbabilityMeasure X` with sets of `Measure X`, freeze
binder order and universes, and check that mathlib's topology is exactly weak convergence.

## Explicit exclusions

- Only one direction of Prohorov's theorem.
- A finite, discrete, compact-space, or single-sequence special case as the root theorem.
- Finite measures of unbounded total mass, vague convergence, or a Levy-Prokhorov metric statement
  without a checked equivalence to the weak-topology claim.
- Treating the legacy `StatementShape` or a theorem-name match as accepted rev-5.6 closure.
