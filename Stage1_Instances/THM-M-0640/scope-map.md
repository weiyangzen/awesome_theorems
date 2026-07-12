# Scope map

## Received scope

The repository fixes only the title `布劳威尔不动点定理`, the literal gloss
`n维球到自身的连续映射有不动点`, Luitzen Brouwer, the year 1910, importance "high", and an
untrusted `已验证` label. The point-set-topology category, execution rank, intake score, and lane
are scheduling metadata and add no mathematical assumptions.

## Candidate mathematical boundary

The familiar closed-ball formulation may be selected only after an accepted source fixes:

- whether the domain is a closed rather than open ball and whether it is the unit ball or a ball
  with an explicitly quantified center and positive or nonnegative radius;
- the real scalar field and the model of n-dimensional Euclidean space, including whether `n` is a
  natural number or a finite index type and how dimension zero is treated;
- whether the map has the ball subtype as both domain and codomain, or is an ambient map with an
  explicit `MapsTo` premise;
- whether continuity is continuity of a subtype map, global ambient continuity, or `ContinuousOn`
  on the ball;
- the exact existential conclusion and fixed-point equality orientation;
- all ordered binders, universes, typeclasses, nonemptiness assumptions, and boundary cases.

These are proposition-selecting or formal-identity/transport-requiring choices, not Lean notation
that intake may fill in by convention.

## Ambiguities and boundary cases

1. `ball` can mean an open metric ball, a closed topological n-ball, or imprecisely its boundary
   sphere. The classical compact theorem uses the closed ball; an open-ball self-map formulation
   can fail, and a sphere self-map theorem is a different claim.
2. A radius-zero closed ball is a singleton, while a negative-radius metric closed ball is empty.
   A variable-radius statement must say which cases it includes.
3. For dimension zero, the Euclidean unit closed ball is a singleton under the standard model;
   excluding or including it changes the quantified domain.
4. A subtype continuous self-map and an ambient map with `ContinuousOn` plus `MapsTo` require a
   checked transport before sharing statement credit.
5. A theorem for a compact convex subset of Euclidean space is classically related to the ball
   theorem, but that relationship is not definitional and no transport is accepted here.
6. Center-zero/unit-radius normalization, arbitrary centers and positive radii, and arbitrary
   finite-dimensional real normed spaces likewise require explicit source and transport decisions.

## Neighbor and substitution exclusions

- `THM-M-0319`, the separate functional-analysis Brouwer target with compact-convex Euclidean
  wording, as a statement or evidence source without an accepted identity and transport decision.
- `THM-M-0636`, the generic point-set-topology fixed-point target, or Schauder, Tychonoff,
  Kakutani, Banach, Lefschetz, Nielsen, or order-theoretic fixed-point theorems as substitutes.
- An interval-only, simplex-only, finite-type, or one-dimensional special case presented as the
  general n-dimensional ball theorem.
- A structure or premise that stores the desired fixed point and projects it as a purported proof.
- The catalog's `已验证` label, a bibliography record, adjacent APIs, or a passing discovery probe
  treated as exact statement, source, or proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, adjacent APIs include
`EuclideanSpace`, `Metric.closedBall`, `Continuous`, `ContinuousOn`, `Set.MapsTo`,
`Function.IsFixedPt`, and `Function.fixedPoints`. The discovery-only probe checks these names. A
bounded search found no terminal Brouwer fixed-point declaration in the repo-local
`Formalizations/Lean/AwesomeTheorems` tree or pinned mathlib tree. That result is not an exhaustive
anchor audit or proof of global absence.

Before statement execution, accountable reviewers must pin an immutable source; select an exact
proposition and incorporated definitions; resolve the ball, dimension, self-map, continuity,
conclusion, and boundary conventions; decide identity and transport relative to `THM-M-0319` and
`THM-M-0636`; audit corrections and errata; approve a translation; and independently review the
crosswalk.
