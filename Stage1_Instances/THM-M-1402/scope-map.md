# Scope map

## Included topic boundary

- A source-selected alphabet `A`, with exactly the discrete, topological, measurable, or measure
  structure required by the eventual proposition.
- A one-sided symbolic space `A^Nat` or two-sided symbolic space `A^Int`, as fixed by the source.
- The coordinate shift convention, typically `sigma(x)(n) = x(n + 1)`, with left/right terminology
  and the indexing operation made explicit.
- A full shift or a source-defined subset, with the exact closure condition proved rather than
  silently assumed: forward closure, surjective restriction, or closure under both shift and
  inverse are distinct.
- Exactly the source-stated proposition or conclusion bundle, including all alphabet, compactness,
  finiteness, invariance, or nonemptiness hypotheses and every conjunct.

## Ambiguities to resolve at statement freeze

The repository wording does not determine:

1. Whether sequences are indexed by `Nat`, `Int`, another monoid/group, or a multidimensional
   lattice.
2. Whether the symbolic space is the full product or a subshift defined by forbidden words,
   closure, or orbit invariance.
3. Whether the alphabet is finite, nonempty, discrete, compact, measurable, or equipped with a
   probability distribution.
4. Whether "shift" means the left shift, its inverse on a two-sided space, or a right shift with a
   supplied predecessor symbol on a one-sided space.
5. Whether the missing proposition asserts the coordinate formula, continuity, surjectivity,
   injectivity/homeomorphism, preservation of a subset or measure, periodic-point behavior,
   transitivity/mixing, dense periodic points, or an entropy formula.
6. How empty or singleton alphabets, empty subshifts, constant sequences, period zero, and
   nonminimal periods are treated.
7. For a subspace, whether only `sigma '' X` is contained in `X`, equality is required, or the
   two-sided space must be invariant under both shift and inverse.

## Explicit exclusions

- Treating the definition of a shift map as a theorem merely because the source inventory calls
  the record a mathematical proposition.
- Choosing continuity as the conclusion when the source states no property, or replacing it with
  surjectivity, homeomorphism, mixing, density of periodic points, or entropy.
- Replacing the target by the neighboring symbolic-dynamics topic, a horseshoe conjugacy theorem,
  a Bernoulli shift, or a theorem about topological or measure entropy.
- Using integer/bit shifts, category-theoretic shifts, stream tail lemmas, or reindexing
  homeomorphisms as source-statement matches merely because they share the word "shift".
- Assuming the desired invariance or dynamical property as a structure field and projecting it.
- Crediting the repository label `已验证` as human-source or Lean kernel evidence.

No canonical Lean target is frozen at intake because the repository record contains no proposition.
