# Source-statement crosswalk

## Candidate sources

- M. Schilder, "Some asymptotic formulas for Wiener integrals," *Transactions of the American
  Mathematical Society* 125 (1966), 63-85. This is the historical primary-paper candidate; its
  exact numbered result, hypotheses, notation, and any corrections require direct inspection.
- A. Dembo and O. Zeitouni, *Large Deviations Techniques and Applications*, second edition,
  Springer, 1998, Section 5.2 (Schilder's theorem). This is a modern interpretation candidate;
  exact theorem/page and edition errata remain to be checked.

These are discovery anchors, not `H0` evidence. Intake does not infer exact wording from the theorem
name or from secondary summaries.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| Schilder's theorem | small-noise Wiener LDP | one exact LDP declaration | included; encoding open |
| Brownian paths | Wiener law on based continuous paths | Brownian process law and path-space measure | included; API open |
| small noise | pushforward by `sqrt epsilon` scaling | measurable scaling map and pushforward | included; convention open |
| LDP | open lower and closed upper bounds | topology, measures, `liminf`/`limsup`, speed | included; library anchor open |
| rate function | Cameron-Martin energy or infinity | absolute continuity, a.e. derivative, `L2` integral, `ENNReal`/extended real | included; encoding open |
| good rate | compact sublevel sets | compactness in uniform topology | included pending source scope |

## Evidence boundary

No repo-local Lean declaration has been accepted or inspected for this intake. The statement and
anchor-audit phases must search the pinned mathlib revision and credible Lean projects, recording
exact modules, declaration types, revisions, axioms, and proof-body provenance. Before `H0`, an
independent reviewer must verify a chosen edition, exact theorem/page, assumptions, normalization,
definitions, and errata, then approve the row-by-row source-to-Lean map.
