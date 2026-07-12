# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory gives Hermann Kunneth, the year 1923, and only the phrase "homology groups
of product spaces". Its `已验证` label is untrusted under rev-5.6 and supplies no coefficient ring,
hypotheses, exact sequence, map, grading, or theorem locator.

A historical primary candidate is Hermann Kunneth, *Uber die Bettischen Zahlen einer
Produktmannigfaltigkeit*, **Mathematische Annalen** 90 (1923), 65-85. A modern source candidate is
Allen Hatcher, *Algebraic Topology* (2002), the section on the Kunneth formula. These entries are
discovery anchors only: an immutable edition has not been inspected row by row, exact theorem/page
and definitions have not been selected, and errata and independent review remain open. They are not
They do not constitute `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "product spaces" | topological spaces `X`, `Y` and their product | concrete spaces and product topology | family fixed; hypotheses open |
| "homology groups" | singular, reduced/unreduced, graded coefficient homology | concrete homology functor and grading | theory intended; conventions open |
| tensor contribution | sums of `H_p(X) tensor H_q(Y)` in total degree | graded tensor/direct sum and cross-product map | required; ring and indexing open |
| torsion correction | degree-shifted Tor terms | concrete `Tor` object and exact-sequence maps | required when source variant includes it |
| Kunneth conclusion | natural isomorphism or short exact sequence | isomorphism or exactness declaration | exact strength unresolved |
| splitting | algebraic splitting, possibly noncanonical | existence/choice/naturality statement | inclusion and strength unresolved |
| 1923 / Kunneth | historical locator | no machine-proof credit | candidate paper identified only |

## Human and machine boundary

The repository-wide search found no theorem-specific Lean artifact for `THM-M-0532`. A text search
of pinned mathlib found no declaration named for Kunneth; that narrow observation is not the later
formal-anchor audit and does not establish absence of reusable homological-algebra components.

Before `H0`, an independent reviewer must select an immutable source edition and exact proposition,
verify its definitions, assumptions, maps, grading, coefficient conventions, and errata, and approve
the row-by-row mapping. Before statement credit, those choices must map to one elaborated Lean target
without dropping the Tor term, adding unjustified freeness, replacing exactness by a dimension
identity, or crediting a noncanonical splitting as natural.
