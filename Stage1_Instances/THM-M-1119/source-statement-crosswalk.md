# Source-statement crosswalk

## Repository record and primary-source lead

The repository inventory supplies the title "Kesten theorem", Harry Kesten, the year 1980, and
the gloss "critical probability of two-dimensional percolation". Its `已验证` field is explicitly
untrusted under rev-5.6. It supplies no theorem number, page, definitions, hypotheses, or formal
artifact and therefore cannot alone identify an exact proposition.

The close primary-source lead is Harry Kesten, *The critical probability of bond percolation on
the square lattice equals 1/2*, **Communications in Mathematical Physics** 74 (1980), 41-59. The
title matches the likely intended equality and the repository year. This intake records the
bibliographic lead for later inspection; it has not inspected and pinned an edition page by page,
selected an exact numbered or displayed result, checked errata, or obtained independent review.
It is discovery evidence, not `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "two-dimensional" | the infinite planar square lattice and its dual | locally finite graph on `Z x Z`, edge relation, duality or checked encoding | likely square lattice; exact encoding open |
| "percolation" | independent Bernoulli bond percolation | product measure on edge configurations and measurable connectivity events | bond model indicated by source title; definitions open |
| "critical probability" | exact definition of `p_c` and percolation probability | real infimum/supremum, parameter domain, infinite-cluster event | intended invariant identified; convention open |
| "equals 1/2" | both inequalities and endpoint behavior required by the selected root | rational/real coercion and equality of the defined critical value | intended equality identified; no Lean target |
| Harry Kesten / 1980 | authorship and bibliographic disambiguation | no machine-proof credit | consistent with lead; pinpoint review open |

## Human and machine boundary

The repository-wide theorem-name search found no existing theorem-specific Lean artifact for
`THM-M-1119`. This intake does not perform the later exhaustive mathlib/external-project anchor
audit and makes no claim about availability of the full percolation result in Lean 4.

Before `H0`, an independent reviewer must inspect an immutable primary edition, record exact
statement and definition locators, map every assumption and endpoint, check errata and later
corrections, and approve the row-by-row mapping. Before statement credit, that selected claim must
be elaborated in Lean without changing bond to site percolation, replacing the infinite lattice by
finite boxes, omitting one inequality, assuming critical behavior, or hiding the conclusion in a
definition.
