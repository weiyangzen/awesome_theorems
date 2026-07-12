# Source-statement crosswalk

## Source anchors

- Norman E. Steenrod, "Products of cocycles and extensions of mappings," *Annals of Mathematics*,
  Second Series 48 (1947), 290-320. This is the identified historical primary paper behind the
  repository's author/date/description. Its exact numbered results, hypotheses, and page-level
  mapping have not yet been inspected in a stable scan.
- Norman E. Steenrod and David B. A. Epstein, *Cohomology Operations*, Annals of Mathematics Studies
  50, Princeton University Press (1962). This is a later primary monograph candidate for a coherent
  existence-and-properties statement. Edition, theorem/page, and errata remain to be audited.

These bibliographic anchors justify `H1`, not `H0`. The Stage0 source only says "stable cohomology
operations on mod-2 cohomology" and marks them verified; it does not state quantifiers, the space
category, conventions, or a proof citation.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "mod-2 cohomology" | coefficients in `F_2` | a concrete mod-2 singular cohomology functor | included; API open |
| "operations" | the indexed family `Sq^i` | degree-shifting maps/natural transformations | included |
| "stable" | compatibility with suspension | checked suspension comparison square | included; convention open |
| Steenrod rather than zero operations | identity, instability, and top-square laws | equalities for `Sq^0`, `i > n`, and `Sq^n` | included |
| all spaces/classes | naturality in the source-exact category | functorial map compatibility | included; category open |

## Required source audit

Before `H0`, a reviewer must inspect an immutable copy of the selected source and record exact
edition, theorem numbers/pages, definitions of cup-`i` and `Sq^i`, every space and coefficient
hypothesis, suspension and indexing conventions, proof boundaries, and known errata. Each frozen
clause must then map to a source node and to the canonical Lean expression.

Before any `M0` claim, anchor audit must search the pinned mathlib revision and credible Lean 4
projects for concrete cohomology-operation declarations. A name match, an abstract operations
structure, or APIs for cup products alone are discovery evidence only.
