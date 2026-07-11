# Scope map

## Included claim

- A sequence `mu n` and a specified limit `mu0` of probability measures.
- A finite-dimensional real inner product space with its Borel measurable structure.
- Weak convergence expressed by convergence in the topology on probability measures.
- Pointwise convergence, for every frequency vector, of characteristic functions to that of
  `mu0`.
- Both implications, packaged as an equivalence.

## Decisions deferred to statement phase

The statement phase must freeze universe levels, typeclass binder order, the exact topology used by
`ProbabilityMeasure`, coercions to measures in `charFun`, and whether the source theorem is stated
only over `Real` or over finite-dimensional real inner product spaces. It must also check the zero-
dimensional space, repeated measures, and nonconvergent sequences as boundary cases.

## Explicit exclusions

- The stronger existence theorem for an arbitrary pointwise limit continuous at zero.
- Tightness alone, continuity of one characteristic function, or uniqueness of distributions.
- Convergence of moments, almost-sure convergence, or convergence in probability as substitutes.
- The legacy `StatementShape` or an upstream theorem name as accepted rev-5.6 proof credit.

The selected known-limit claim appears compatible with mathlib's existing probability-measure and
characteristic-function APIs, but compatibility and minimal imports belong to the statement phase.
