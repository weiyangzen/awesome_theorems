# Scope map

## Included claims

### Downward direction

- A first-order language `L`, a nonempty `L`-structure `M`, a distinguished subset `A` of `M`, and
  an infinite cardinal `kappa`.
- Cardinal bounds `|A| <= kappa`, `|L| <= kappa`, and `kappa <= |M|` (with universe lifts made
  explicit by the later Lean statement).
- An elementary substructure `N` of `M` containing `A`, with cardinality exactly `kappa`.

### Upward direction

- A first-order language `L`, an infinite `L`-structure `M`, and a cardinal `kappa` satisfying
  `|L| <= kappa` and `|M| <= kappa`.
- An `L`-structure `N` of cardinality exactly `kappa` together with an elementary embedding of `M`
  into `N`; this is the elementarily embedded extension encoding.

The root theorem is a paired result with both clauses. Closing only one direction cannot close this
target. The intended language cardinal is the cardinality of its function and relation symbols, as
defined by the selected source and mapped explicitly to mathlib's `FirstOrder.Language.card`.

## Statement encoding decisions

`Stage1Instances.THM_M_0648.CanonicalTarget` represents the pair as a conjunction of named downward
and upward propositions. Its ordered binders, universes, and cardinal lifts are frozen in
`Statement.lean`; `canonicalTarget_iff_expanded` is the checked assembly expansion. The later source
audit must still cross-check whether the selected primary source packages the lower bounds with a
maximum and whether its upward terminology maps to the selected elementary-embedding encoding.

Boundary cases requiring explicit treatment are `A = empty`, `kappa = aleph_0`, `kappa = |M|`, an
empty language, finite `M` (excluded from the upward clause), and equality rather than strict growth
in the upward cardinal bounds. No proper-extension conclusion is currently claimed when
`kappa = |M|`.

## Explicit exclusions

- The combined direction-selecting Loewenheim-Skolem wrapper as a substitute for separately mapping
  and closing both the upward and downward clauses.
- The existence of merely an elementarily equivalent model without the required embedding or
  substructure relation.
- The compactness theorem, completeness theorem, Skolem normal form, or Skolemization alone.
- Second-order logic, infinitary languages, many-sorted variants, and finite-model analogues unless
  a later checked transport explicitly maps them to this first-order target.
- Any structure/package that assumes either desired construction as a field.

The manifest phrase "change of model cardinality" is too weak by itself. The quantified hypotheses,
elementarity relation, containment requirement, and exact cardinal equalities above are part of the
frozen human scope and may not be dropped to obtain an easier theorem.
