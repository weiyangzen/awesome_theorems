# Scope map

## Included theorem family

- A source-specified Bernoulli base probability space or alphabet with weights.
- The corresponding one-sided or two-sided product probability space.
- A precisely oriented coordinate shift with the measurability and invertibility properties required
  by the selected source.
- Exactly one source-selected theorem about that system: construction, measure preservation,
  ergodicity, mixing, entropy, or classification.
- Any measure-theoretic isomorphism notion, completion convention, entropy hypotheses, and
  nondegeneracy assumptions used by that exact theorem.

## Ambiguities to resolve at statement freeze

The repository wording does not determine:

1. Whether "Bernoulli shift" is a definition/construction or names a theorem about such a system.
2. Whether configurations are indexed by `Nat`, `Int`, another semigroup/group, or a general group
   action, and whether the shift is left or right.
3. Whether the alphabet is finite, countable, or a standard probability space, and whether zero
   weights or infinite entropy are allowed.
4. Whether the intended result is product-measure invariance, ergodicity, strong mixing, a
   Kolmogorov property, an entropy formula, or classification up to measure-theoretic isomorphism.
5. Whether isomorphisms and conjugacy equations are pointwise or modulo null sets and whether
   measures and sigma-algebras are completed.
6. Whether a classification claim concerns equal base distributions, equal entropy, factors, or
   some other invariant.

## Explicit exclusions

- A bare definition of a coordinate-shift function presented as proof of a classification theorem.
- Measure preservation, ergodicity, mixing, and entropy treated as interchangeable conclusions.
- A finite cyclic coordinate permutation substituted for a one- or two-sided infinite shift.
- An i.i.d. family theorem or Bernoulli random-variable distribution used as a substitute for a
  dynamical-system result.
- Ornstein's entropy classification imported into this target without resolving the separately
  scheduled `THM-M-1408` and proving that the source intended that duplicate reading.
- A weakened special case chosen solely because current mathlib has convenient APIs.
- The repository's `已验证` label as evidence of a primary human proof or Lean kernel closure.

No canonical Lean target is frozen at intake because no exact source theorem has been selected.
