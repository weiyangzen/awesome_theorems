# Source-statement crosswalk

## Candidate sources

- Christer Borell, "The Brunn-Minkowski inequality in Gauss space," *Inventiones mathematicae*
  30 (1975), 207-216. This is a primary historical candidate for the Gaussian isoperimetric
  result. The exact theorem number, hypotheses, wording, and any errata have not yet been inspected.
- Michel Ledoux, *The Concentration of Measure Phenomenon*, AMS Mathematical Surveys and
  Monographs 89 (2001). This is a modern secondary exposition candidate for normalization and
  equivalent formulations; its exact theorem/page must be inspected before receiving source credit.

These bibliographic anchors support discovery only, not `H0`. The independent Sudakov-Tsirelson
historical route must also be checked during source audit rather than inferred from secondary
attribution.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Gaussian measure's isoperimetric inequality" | half-spaces minimize Gaussian boundary/enlargement | standard Gaussian measure on Euclidean space | included; normalization open |
| measurable set | arbitrary measurable `A` | measurable set and measure value | included |
| neighborhood/enlargement | metric thickening by `r >= 0` | distance-to-set or Minkowski enlargement | included; open/closed convention open |
| equal-measure half-space | comparator determined by a Gaussian quantile | half-space measure/CDF correspondence | included; endpoint convention open |
| extremal inequality | `A` has no smaller enlargement | measure inequality or equivalent boundary statement | included; exact source form open |

## Repository boundary

The Stage0 and legacy Stage1 prose provide only a theorem name and the clarifying phrase
"Gaussian measure's isoperimetric inequality." They contain no exact statement or Lean artifact and
receive no proof credit. Before `H0`, review must identify a stable edition and exact theorem/page,
check definitions and assumptions against the source, investigate errata, and approve every
source-to-Lean row. Before `M0`, the exact expression must elaborate and close in the pinned
environment without placeholders or untracked external proof bodies.
