# Source-statement crosswalk

## Repository evidence

The source inventory at `Docs/researches/math_theorems.md:6222` records only the Chinese label
"Erdos-Renyi random graph," attribution to Erdos/Renyi, the year 1959, and the phrase "basic theory
of the random-graph model." The Stage0 projection at `Docs/Stage0_Blueprint.md:23144` explicitly
leaves definitions, assumptions, proof route, dependencies, axioms, formal artifacts, and formal
system open. Neither record supplies a theorem number, quantifiers, hypotheses, conclusion, or
edition. The `已验证` field is untrusted metadata and is not H, M, or R evidence.

## Inspected primary-family lead

Paul Erdos and Alfred Renyi, *On Random Graphs I*, *Publicationes Mathematicae Debrecen* 6 (1959),
290-297, was inspected through the Renyi Institute scan at
`https://www.renyi.hu/~p_erdos/1959-11.pdf` (observed SHA-256
`b41fac16a7ee513f9651dcf8d645ed62742cdf970f81fc7b0f866d6168e8108a`). Page 290 defines a random
graph on `n` possible labelled vertices by choosing uniformly among graphs having exactly `N`
edges; isolated vertices remain part of the graph. Pages 290-291 announce four different results:
a connectivity limit, two component-count laws, and a connectivity stopping-time law.

This inspection identifies the historical fixed-edge model and a theorem family, but the catalog
does not select one of the four results. The scan has not been admitted as a repository-owned
immutable source, its complete definition/proof/errata boundary has not been independently
reviewed, and no exact result has been approved. It therefore provides discovery evidence only and
no H0 credit.

## Distinct modern-name lead

Edgar N. Gilbert, *Random Graphs*, *The Annals of Mathematical Statistics* 30(4) (1959),
1141-1144, DOI `10.1214/aoms/1177706098`, is the primary bibliographic lead for the
independent-edge model commonly called `G(n, p)`. Crossref metadata was inspected, but the primary
text, definitions, theorem statements, proof, and corrections were not admitted or independently
reviewed. Its model cannot be substituted for the catalog's Erdos/Renyi attribution without an
explicit source decision and checked mathematical mapping.

## Phrase-to-statement crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Erdos-Renyi random graph" | historically `G(n, m)`; modern usage may also mean `G(n, p)` | one selected law or an explicit variant tag | ambiguous; no variant selected |
| "random graph model" | probability distribution on finite simple graphs | concrete finite graph sample type plus `Measure`/`PMF` | family identified; exact encoding open |
| fixed `N` edges in the 1959 paper | uniform law on labelled graphs with exactly `N` edges | edge-count subtype/event and uniform finite law | inspected source definition; not selected as root |
| independent edges | Bernoulli product law | edge indicators, parameter in `[0,1]`, and independence | Gilbert/mathlib candidate only |
| "basic theory" | no truth-valued conclusion | an exact `Prop`, not merely a definition or topic | hard statement blocker |
| 1959 paper Theorems 1-4 | four non-equivalent asymptotic conclusions | separate limit/event/stopping-time propositions | none selected; neighbor collisions unresolved |
| authors/year/status | bibliographic metadata | no kernel content | locator only; no proof credit |

## Pinned Lean discovery boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs`. It defines
`SimpleGraph.binomialRandom`, the `G(V, p)` probability measure, and proves map, application,
endpoint, probability-measure, and singleton-mass facts. The module itself notes that calling this
the Erdos-Renyi model is historically inaccurate because Erdos and Renyi introduced a related but
different model.

These declarations are useful `G(n, p)` infrastructure, not a source-frozen proposition for
`THM-M-0848`. The same module has an explicitly unfinished desired edge-count-distribution result;
no such open interface is credited. The intake probe elaborates only completed adjacent APIs. A
bounded repository and pinned-mathlib search found no `THM-M-0848`-specific exact statement. This
is intake discovery, not the exhaustive formal-candidate audit assigned to the later anchor phase.

## Source gate and retry condition

Before statement credit, an independent reviewer must preserve and approve an immutable primary
edition, select one exact numbered result (or formally justify another proposition matching the
catalog), map all incorporated definitions and assumptions, check corrections/errata, and resolve
the collisions with targets `THM-M-0849` through `THM-M-0852` and duplicate `THM-M-1112`. The
approved result must then receive a row-by-row map to an elaborated Lean expression and the required
statement mutations. No source fidelity, formal closure, or theorem completion is claimed here.
