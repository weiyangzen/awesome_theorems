# Source-statement crosswalk

## Repository record and primary-source lead

The repository inventory supplies the title "Kesten theorem", Harry Kesten, the year 1980, and
the gloss "critical probability of two-dimensional percolation". Its `已验证` field is explicitly
untrusted under rev-5.6. It supplies no theorem number, page, definitions, hypotheses, or formal
artifact and therefore cannot alone identify an exact proposition.

The close primary-source lead is Harry Kesten, *The critical probability of bond percolation on
the square lattice equals 1/2*, **Communications in Mathematical Physics** 74 (1980), 41-59. The
title matches the intended equality and the repository year. The statement phase selects the
equality literally stated by that title as its root and records DOI `10.1007/BF01197577`, volume 74,
issue 1, and pages 41-59. It has not yet performed a page-by-page definition crosswalk, checked
errata, or obtained independent review. The selection fixes the Lean statement boundary but is not
`H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "square lattice" | infinite nearest-neighbor graph on `Z x Z` | `SquareLattice : SimpleGraph (Int x Int)` and its `edgeSet` | frozen and elaborated; source-definition review open |
| "bond percolation" | independent Bernoulli state on each unoriented bond | `Configuration`, `bondMeasure`, and `Measure.infinitePi` | frozen and elaborated; measurability/proof obligations open |
| "critical probability" | infimum of parameters with positive rooted infinite-cluster probability | `OriginInInfiniteCluster`, `percolationProbability`, `criticalProbability` | frozen and elaborated; source-convention review open |
| "equals 1/2" | exact threshold equality | `KestenTarget : criticalProbability = (1 / 2 : NNReal)` | frozen and elaborated; unproved |
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
