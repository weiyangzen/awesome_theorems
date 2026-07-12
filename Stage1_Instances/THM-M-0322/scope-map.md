# Scope map

## Included claim

- A real locally convex Hausdorff topological vector space `E`.
- A compact convex subset `s` of `E`.
- Extreme points defined intrinsically relative to `s`.
- Equality of `s` with the topological closure of the real convex hull of those extreme points.
- The empty-set boundary case, for which both sides are empty and no separate nonemptiness premise
  is needed.

## Decisions for the statement phase

The statement phase must freeze the exact Lean structures supplying the topological vector-space
assumptions, universe and binder order, notation expansion, and the definitions of `extremePoints`,
`convexHull`, and `closure`. It must compare the pinned candidate's elaborated expression with the
human claim and mutation-test removal of compactness and convexity, a changed scalar/domain, changed
binder scope, and the empty-set boundary.

The source review must also determine whether the selected historical or modern theorem says
"locally convex space" with an implicit Hausdorff convention, and whether "closed convex hull" is
defined directly or as closure of the convex hull. Any credited equivalence needs a checked Lean
transport.

## Explicit exclusions

- The Krein-Milman lemma asserting only existence of an extreme point in a nonempty compact set.
- Minkowski-Caratheodory or finite-dimensional variants where closure can be omitted.
- The Banach-Alaoglu theorem, Choquet representation by probability measures, or Milman's converse.
- A theorem restricted to normed, Banach, finite-dimensional, complex, or weak-star settings as a
  substitute for the stated locally convex real-space theorem.
- A one-sided inclusion, density statement without checked equality transport, or an abstract
  package assuming the desired equality as data.
- The repository label `已验证`, a successful API probe, or the presence of a named mathlib theorem
  as proof or release evidence.

No canonical Lean expression hash is frozen during intake; that is the next DAG node's gate.
