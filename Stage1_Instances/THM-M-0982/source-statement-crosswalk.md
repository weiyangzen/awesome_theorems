# Source-statement crosswalk

## Candidate primary sources

- Patrick Billingsley, *Probability and Measure*, third edition, Wiley (1995), the introductory
  probability-measure chapter's continuity properties. Exact theorem number, page, hypotheses, and
  errata have not yet been inspected.
- Olav Kallenberg, *Foundations of Modern Probability*, second edition, Springer (2002), the opening
  measure/probability chapter's monotone continuity results. Exact lemma/page, edition wording, and
  errata have not yet been inspected.

These are discovery candidates, not `H0` evidence. The statement phase must inspect a stable edition
and record a pinpoint theorem/page, definitions, assumptions, and errata before source fidelity can
be accepted.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "continuity of probability" | continuity from below and above | two `Tendsto` claims or an exact checked conjunction | included; source wording open |
| increasing events | `A_n` nested upward | `Monotone A`, countable union, measure convergence | included; encoding open |
| decreasing events | `A_n` nested downward | `Antitone A`, countable intersection, measure convergence | included; hypotheses open |
| probability measure | countably additive measure of total mass one | `Measure` plus `IsProbabilityMeasure`, or `ProbabilityMeasure` | included; representation open |
| event regularity | source measurability assumptions | `MeasurableSet` or `NullMeasurableSet` | decision deferred to exact source |

## Existing Lean boundary

The legacy `S1_M_262.lean` defines a conjunction over `Measure` and `IsProbabilityMeasure` and names
`tendsto_measure_iUnion_atTop` and `tendsto_measure_iInter_atTop`. It is valuable candidate evidence,
but its imports, declaration types, terminal bodies, axioms, pinned dependency revision, and exact
match to the selected human source must be freshly audited. No legacy `#check`, wrapper, or status
label is accepted by this intake.

Before `H0`, an independent reviewer must approve the selected edition and a row-by-row mapping of
all assumptions and boundary cases. Before machine credit, the statement and later anchor phases
must elaborate the exact target and inspect the actual terminal proof-body provenance.
