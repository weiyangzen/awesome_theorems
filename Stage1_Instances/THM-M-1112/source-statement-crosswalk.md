# Source-statement crosswalk

## Repository evidence

The Stage0 record supplies only the Chinese name "random graph", the phrase "Erdos-Renyi random
graph model", attribution to Paul Erdos and Alfred Renyi, the year 1959, and the untrusted status
`已验证`. The research inventory similarly says "basic theory of the random graph model". Neither
record gives a theorem, quantifiers, hypotheses, conclusion, edition, page, or proof boundary.

## Candidate primary sources

- Paul Erdos and Alfred Renyi, *On Random Graphs I*, Publicationes Mathematicae Debrecen 6 (1959),
  290-297. This is the historical primary candidate for the fixed-edge model and associated
  asymptotic results.
- Edgar N. Gilbert, *Random Graphs*, Annals of Mathematical Statistics 30 (1959), 1141-1144. This
  is a primary candidate for the independent-edge model often grouped under the modern
  "Erdos-Renyi" name.

These citations are discovery anchors only. The papers, exact theorem/page, definitions, hypotheses,
and errata have not been independently inspected for this intake, so they provide no `H0` credit.
The attribution difference is material: the modern umbrella name must not erase which construction
and which source actually support the selected claim.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "random graph" | probability distribution on finite simple graphs | finite graph sample type plus probability measure/PMF | family identified; exact encoding open |
| "Erdos-Renyi" | historically related `G(n, m)` and modern-name `G(n, p)` models | an explicit variant tag or one selected law | ambiguous; must be resolved from source |
| `G(n, m)` | uniform law conditioned on exactly `m` edges | finite uniform distribution and edge-count predicate | candidate variant only |
| `G(n, p)` | mutually independent Bernoulli edge indicators | product/Bernoulli law and independence certificate | candidate variant only |
| "model" / "basic theory" | no unique theorem-level conclusion | exact proposition, not merely a definition | hard statement blocker |
| 1959 / authors | bibliographic locator | no kernel content | metadata only |

## Source and machine boundary

A repository-wide text search found no theorem-specific Lean module for `THM-M-1112`. Hits for
"Erdos-Renyi" in `S1_M_289.lean` concern the Erdos-Renyi/Kochen-Stone extension of Borel-Cantelli,
not this random-graph target. This negative local search is not the required pinned mathlib and
external-project anchor audit.

Before statement credit, an independent reviewer must select and inspect a source result, including
its exact page, definitions, assumptions, limiting regime, and errata, and approve a row-by-row map
to an elaborated Lean expression. Before `H0`, the proof boundaries and every source-dependent
convention must also be reviewed. No source or machine closure is claimed here.
