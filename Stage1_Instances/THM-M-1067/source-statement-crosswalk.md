# Source-statement crosswalk

## Candidate sources

- Paul Levy, *Processus stochastiques et mouvement brownien*, Gauthier-Villars, Paris, 1948. This
  is the historical primary-monograph candidate indicated by the Stage0 attribution and date; its
  exact result, page, notation, hypotheses, and later-edition changes require direct inspection.
- Daniel Revuz and Marc Yor, *Continuous Martingales and Brownian Motion*, third edition, Springer,
  1999, Chapter VI (local times). This is a modern source candidate for the jointly continuous
  Brownian local-time field and occupation-times formula; the exact theorem/corollary/page and
  edition errata remain to be checked.

These are discovery anchors, not `H0` evidence. In particular, the intake does not infer a precise
theorem from the short Stage0 phrase "Brownian local time."

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Brownian motion | standard real process starting at zero | probability space, filtration, process, Brownian laws and continuity | included; exact API open |
| local time | nonnegative random field `L(t,a)` | measurable field indexed by time and level | included; construction open |
| occupation density | time spent near each spatial level | equality of time and spatial Lebesgue integrals | included; normalization open |
| jointly continuous version | one version continuous in `(t,a)` | samplewise joint continuity on a probability-one event | included; quantifier order open |
| almost sure identity | simultaneous pathwise formula | measurable full-measure event and quantified test functions/times | included; source scope open |

## Evidence boundary

No repo-local Lean declaration has been accepted or inspected for this intake. A repository search
for the phrases `local time`, `occupation density`, and Brownian/local-time combinations found no
candidate in the available mathlib source tree; that negative keyword search is only intake
orientation, not the required immutable anchor audit.

Before `H0`, an independent reviewer must inspect a chosen edition and verify the exact
theorem/page, assumptions, normalization, quantifier order, definitions, and errata, then approve a
row-by-row source-to-Lean map. The statement and anchor-audit phases must separately inspect pinned
mathlib and credible Lean 4 projects, recording exact modules, declarations, revisions, axioms, and
terminal proof provenance.
