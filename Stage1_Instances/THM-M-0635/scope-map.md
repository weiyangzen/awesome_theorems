# Scope map

## Preserved theorem family

The intake preserves the repository claim that a continuous function on a compact set attains both
a maximum and a minimum. The title, Weierstrass attribution, point-set-topology placement, and
wording identify the compact-domain extreme-value theorem family. A later statement phase must use
an admitted source to freeze one exact proposition rather than infer missing binders from mathlib.

A familiar real-valued candidate, not credited here as the canonical statement, is: for a
nonempty compact subset `K` of a topological space and a function `f : X -> Real` continuous on
`K`, there are points `x_min` and `x_max` in `K` such that every `x` in `K` satisfies
`f x_min <= f x <= f x_max`.

## Proposition-changing decisions

The statement and source-review phases must resolve all of the following:

1. The immutable source edition, exact theorem/page, incorporated definitions, proof boundary,
   translation, correction history, and independent review.
2. Whether the domain is an arbitrary topological space with a compact subset, a compact space,
   a compact interval, or a compact metric subset.
3. Whether the codomain is `Real`, an arbitrary linearly ordered topological space, or another
   source-selected ordered space; the two order-topology hypotheses used by the generic mathlib
   minimum and maximum declarations are not silently inserted into the catalog claim.
4. Whether continuity is `ContinuousOn f K`, global `Continuous f`, or continuity of a function
   defined on the subtype `K`.
5. Whether nonemptiness is explicit, built into a compact-domain carrier, or omitted by the source;
   an empty set cannot supply the required extrema witnesses.
6. Whether the conclusion uses two possibly different witnesses, extrema of the image, `IsMinOn`
   and `IsMaxOn`, explicit inequalities, or a bundled pair, and which checked transports connect
   alternate forms.
7. Ordered binders, universes, typeclasses, coercions, equality and inequality orientation, and the
   selected foundation, TCB, and computation profiles.

These are statement decisions, not proof-search conveniences.

## Boundary and mutation cases

The exact statement must dispose of an empty compact set, a singleton, a constant function, a
noncompact domain, a function continuous only outside the selected set, a codomain lacking the
needed order/topology compatibility, and minimum and maximum attained at different points. It must
also distinguish attainment from boundedness, supremum/infimum existence, uniqueness, strict
extrema, local extrema, and an algorithm for finding extrema. Intake excludes no case silently.

## Neighbor and substitution exclusions

- `THM-M-0633` separately owns uniform continuity of continuous functions on compact sets.
- `THM-M-0634` separately owns the intermediate-value/connected-image family.
- `THM-M-0265` separately owns Weierstrass polynomial approximation, despite the shared
  attribution.
- Maximum-modulus, harmonic or heat-equation maximum principles, optimization existence theorems,
  Fermat's stationary-point theorem, and interval calculus tests are not substitutes.
- A boundedness theorem alone, an image compactness theorem alone, or only one of maximum and
  minimum attainment is weaker than the received two-sided claim.
- A structure or premise storing extrema witnesses, a numerical search, theorem name, API check,
  or the catalog label `已验证` supplies no proof credit.

## Formal boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the generic
declarations `IsCompact.exists_isMinOn` and `IsCompact.exists_isMaxOn` in
`Mathlib.Topology.Order.Compact`, and defines `IsMinOn` and `IsMaxOn` in
`Mathlib.Order.Filter.Extr`. The intake probe authenticates their availability and axiom reports.
It declares no target theorem. Minimal imports for a canonical root, the combined expression,
environment and expression fingerprints, checked transports, and four required mutation classes
belong to `S56-M-0635-STATEMENT`.
