# Scope map

## Preserved catalog boundary

The repository fixes target `THM-M-0213`, the name `双曲平行公设`, the Lobachevsky/Bolyai
attribution, the year 1830, and the gloss `过直线外一点可作无数条平行线`. Intake preserves the
recognizable hyperbolic-parallel-postulate family: a line, a point external to that line, and an
infinite family of distinct nonintersecting lines through that point. This sentence is a topic
boundary, not an accepted canonical proposition.

## Proposition-changing decisions

An approved source and statement run must freeze all of the following:

- whether the ambient object is a source-defined synthetic neutral/hyperbolic plane, the Poincare
  disk, the Poincare upper half-plane, the Klein model, or another interpretation;
- the complete incidence, betweenness, congruence, continuity, dimension, and nondegeneracy axioms,
  and whether the parallel clause is assumed or derived;
- the representation and extensional equality of points and complete lines, including whether a
  line is determined by points, a geodesic image, an affine subspace, or another primitive object;
- the exact premise that the point lies outside the line and whether every line is required to be
  inhabited, proper, or determined by two distinct points;
- whether a candidate through-line must contain the external point and be distinct from the given
  line, and how distinct candidate lines are counted;
- the meaning of parallel: no common finite point, limiting/asymptotic at an ideal endpoint,
  ultraparallel, or a source-defined union of these classes;
- the meaning of "infinitely many": `Set.Infinite`, an injection `Nat -> Line`, arbitrarily large
  finite families, a continuum-cardinality statement, or an interval/fan parametrization;
- whether the root asserts at least two limiting parallels plus the intervening disjoint fan, all
  disjoint through-lines, a classification of limiting and ultraparallel lines, or only infinitude;
- whether ideal/boundary points participate in incidence or intersections and how orientation and
  the two sides of the original line are treated; and
- all ordered binders, universes, structures, typeclass assumptions, hypotheses, conclusions,
  coercions, quotient choices, and exceptional cases.

These choices change the target and sometimes its logical role. They are a resolution ledger, not
a canonical statement.

## Candidate formulations not credited

- A synthetic axiom saying that for every line and external point there are at least two distinct
  lines through the point disjoint from the original line.
- A theorem in a chosen model that the set of all disjoint geodesics through the point is infinite.
- A result identifying two limiting parallels and proving that the geodesics between them form an
  infinite fan of nonintersecting lines.
- The negation of Playfair uniqueness or of Euclid's fifth postulate.
- A cardinality classification, such as continuum many disjoint through-lines.

No item in this list is selected, asserted, or credited at intake. In particular, existence of two
parallels does not by itself establish the catalog's literal infinitude wording without an approved
source relationship or checked derivation.

## Neighbor target boundaries

`THM-M-0217`, `THM-M-0218`, and `THM-M-0219` separately own the Klein, Poincare disk, and Poincare
upper-half-plane models. They may later supply interpretations or proof routes, but their carrier,
metric, and model theorems do not determine this target's synthetic vocabulary or transfer proof
credit without an explicit source-faithful transport. `THM-M-0215` and `THM-M-0220` separately own
the hyperbolic cosine and triangle-area formulas; neither is the parallel postulate.

## Explicit exclusions

- Euclidean affine parallelism, where a unique direction-parallel line passes through an external
  point, substituted for hyperbolic nonintersection.
- A particular disk, upper-half-plane, or Klein encoding chosen only because mathlib has adjacent
  definitions.
- Existence of one or two special parallels presented as the literal infinite-family claim.
- Counting parametrizations that map different parameters to the same geometric line.
- Treating limiting parallels alone, ultraparallels alone, or geodesic rays alone as all lines
  without a source-selected convention.
- A structure that stores the desired infinitude or parallel property as a field, followed by a
  tautological projection.
- The catalog label `已验证`, a theorem name, or an adjacent API elaboration used as H or M evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `UpperHalfPlane` and its Poincare `MetricSpace`
provide an analytic carrier and distance, but the bounded intake search found no synthetic
hyperbolic-line or parallel-postulate declaration. `AffineMap.lineMap` describes ordinary affine
interpolation in affine spaces, not hyperbolic geodesics or disjointness. `Set.Infinite` and
`Set.Infinite.natEmbedding` can encode one possible infinitude conclusion only after the line set
and parallel predicate are source-selected. The probe authenticates these adjacent APIs and no
more; a full immutable formal-anchor audit belongs to a downstream phase.
