# Source-statement crosswalk

## Repository record and candidate source

The repository inventory supplies the title "percolation theory", the year 1957, the names Simon
Broadbent and John Hammersley, and the gloss "percolation thresholds and critical phenomena". Its
`已验证` field is explicitly untrusted under rev-5.6. It gives no theorem number, graph, model,
threshold definition, assumptions, or exact conclusion, so it cannot identify one proposition.

The historical primary candidate matching the names and year is S. R. Broadbent and J. M.
Hammersley, *Percolation Processes. I. Crystals and Mazes*, **Proceedings of the Cambridge
Philosophical Society** 53 (1957), 629-641, DOI `10.1017/S0305004100032680`. This intake records it
only as a discovery anchor: an immutable copy has not been inspected theorem by theorem, and no
numbered result, assumptions, terminology, corrections, or modern equivalence has been approved.
The broad phrase "critical phenomena" may also summarize later developments not asserted in that
paper, so it must not be silently appended to a 1957 result.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "percolation" | bond or site model and its configuration law | graph/lattice, Bernoulli-indexed configuration, measurable product law | family identified; model open |
| "threshold" | exact order parameter and infimum/supremum convention | real parameter interval, percolation event probability, threshold definition | intended component identified; definition open |
| "phase" | below/above-threshold conclusion and endpoint treatment | quantified implications for cluster/connectivity predicates | conclusion and quantifier order open |
| "critical phenomena" | endpoint behavior, continuity, exponents, scaling, or other precise claim | exact limiting/probability proposition, if present in the selected source | too broad for statement credit |
| 1957 / Broadbent-Hammersley | historical source identity | bibliographic provenance only | candidate paper identified; pinpoint review open |
| infinite medium | source's lattice/maze and boundary conventions | infinite locally finite graph and distinguished root or invariant event | graph and rooting open |

## Human and machine boundary

The repository-wide search found no existing theorem artifact for `THM-M-1118`; only the source
inventory and adjacent percolation-family entries were present. This intake does not perform the
later exhaustive formal-anchor audit and makes no claim about external Lean projects or pinned
mathlib support for the full proposition.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
theorem or displayed result and pinpoint locator, map every definition and assumption, check
errata/corrections and historical-to-modern terminology, and approve the row-by-row mapping.
Before statement credit, that selected claim must map to an elaborated Lean target without changing
the percolation model, graph, threshold convention, endpoint, or asserted critical behavior.
