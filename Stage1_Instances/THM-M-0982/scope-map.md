# Scope map

## Included claim

- An arbitrary measurable space and a countably additive probability measure on it.
- An increasing sequence of events, with convergence of their probabilities to the probability of
  their countable union.
- A decreasing sequence of measurable events, with convergence of their probabilities to the
  probability of their countable intersection. Probability normalization supplies finiteness.
- Extended-nonnegative-real convergence in the topology used by mathlib's `Measure` codomain.

## Frozen statement decisions

`Statement.lean` freezes a conjunction of the two laws, `Nat` indexing, ordinary measurable events,
an arbitrary universe-polymorphic measurable space, `Measure` plus `IsProbabilityMeasure`, and
`Tendsto` at `atTop` in `ENNReal`. Empty, universal, and constant event sequences remain included.
The historical null-measurable formulation is credited only as the target of a checked one-way
transport. Pinpoint primary-source review remains open and may not silently alter this formal target.

## Explicit exclusions

- Continuity of a probability density, distribution function, random variable, or stochastic path.
- Finite additivity without countable additivity.
- A single finite-union identity or only the special case of pairwise disjoint events.
- Replacing probability measures by arbitrary measures without retaining the finiteness hypothesis
  needed for continuity from above.
- Treating the historical `StatementShape` or a theorem-name match as rev-5.6 closure.
