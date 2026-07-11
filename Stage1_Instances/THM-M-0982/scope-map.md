# Scope map

## Included claim

- An arbitrary measurable space and a countably additive probability measure on it.
- An increasing sequence of events, with convergence of their probabilities to the probability of
  their countable union.
- A decreasing sequence of events, with convergence of their probabilities to the probability of
  their countable intersection, under the precise measurability/finite-first-term conditions chosen
  from the primary source.
- Extended-nonnegative-real convergence as the likely mathlib representation; this is not yet the
  frozen canonical encoding.

## Statement-phase decisions

The selected primary theorem must fix whether every event is measurable or only null-measurable,
whether continuity from above assumes finite mass of the first event or uses total probability mass
one, and whether the two directions are one theorem or two. It must also settle indexing, empty or
constant sequences, the ambient sigma-algebra, binder order, universes, and the exact topology and
codomain used for convergence.

## Explicit exclusions

- Continuity of a probability density, distribution function, random variable, or stochastic path.
- Finite additivity without countable additivity.
- A single finite-union identity or only the special case of pairwise disjoint events.
- Replacing probability measures by arbitrary measures without retaining the finiteness hypothesis
  needed for continuity from above.
- Treating the historical `StatementShape` or a theorem-name match as rev-5.6 closure.
