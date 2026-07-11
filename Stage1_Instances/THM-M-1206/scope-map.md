# Scope map

## Included theorem family

- The fundamental compactness theorem that extracts a Young measure from a sequence of measurable
  maps, rather than the bare definition of a Young measure.
- A finite measure domain and a finite-dimensional Euclidean (or source-equivalent locally compact
  separable) target, subject to the exact selected source.
- Weak measurability of the parametrized probability measures and the source's convergence formula
  against its admissible class of continuous or Caratheodory integrands.
- The source's precise tightness, convergence-in-measure, uniform-integrability, coercivity, and
  concentration-loss conditions, including whether mass can escape to infinity.

## Decisions required before statement freeze

The statement phase must select and inspect one stable primary theorem and fix the domain measure
space, target topology and Borel structure, sequence measurability, subsequence encoding, almost
everywhere equivalence, probability-kernel measurability, test-function class, integrability mode,
and exact convergence topology. It must state whether the result is the classical bounded/tight
version or Ball's noncompact-target version and whether convergence is pointwise in tests, weak in
`L1`, or convergence of integrals. Null domains, zero measures, non-tight sequences, unbounded
tests, and concentration/escape of mass require explicit treatment.

## Explicit exclusions

- The definition or existence of a constant Dirac-valued kernel in place of subsequence
  compactness.
- Prokhorov compactness for one sequence of probability measures without spatial parametrization.
- A finite-valued sequence or finite probability simplex substituted for the measurable-map
  theorem.
- Jensen's inequality, relaxation, or gradient Young-measure characterization substituted for the
  fundamental generation theorem.
- An abstract structure that assumes the limiting kernel or convergence formula as fields.

The later Lean target must expose the generating sequence, extracted subsequence, parametrized
kernel, measurability, and test-integral convergence, or record a precise library blocker.
