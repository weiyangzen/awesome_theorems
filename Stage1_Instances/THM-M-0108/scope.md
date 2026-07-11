# Scope map

## Included claim

The target is the classical projective analytic-to-algebraic theorem: a closed
complex-analytic subvariety `Z` of finite-dimensional complex projective space
is algebraic. At statement phase, the ambient dimension, complex field,
projective-space model, analytic-subvariety structure, closedness, homogeneous
ideal, and equality of carriers must all be explicit.

The primary carrier formulation says that `Z` is the simultaneous zero set of
a family of homogeneous complex polynomials. A scheme/subspace formulation may
replace it only after a checked transport accounts for reducedness and the
analytic/algebraic structure, not merely equality of underlying sets.

## Exclusions

- Chow's lemma, Chow varieties, Chow groups, and Chow rings.
- The converse direction that algebraic projective subvarieties are analytic.
- GAGA equivalences stronger than the target unless a checked specialization
  produces this exact conclusion.
- Compact analytic spaces not already embedded as closed subvarieties of a
  projective space.
- Abstract predicates such as `ProjectiveAnalyticLocalModel` and
  `HomogeneousPolynomialCutOut` when they carry no native mathematical data.
- Merely showing that the ambient projective scheme is proper.

## Required transports

Later work must choose between reduced closed analytic subsets and analytic
subspaces with nilpotents. It must check any transport among homogeneous-ideal
zero loci, projective algebraic varieties, reduced closed subschemes, and
analytifications. Equality of carriers alone does not establish equality of
structured spaces.

## Statement mutation obligations

Reject variants dropping analytic structure, closedness, projective ambient
space, finite dimension, or the complex base field. Reject conclusions giving
only local algebraicity, constructibility, or containment in an algebraic set.
Test the empty/full subsets and `n = 0`, and detect any silent reducedness or
irreducibility assumption.
