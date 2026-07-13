# THM-M-0870 source-statement crosswalk

## Repository evidence

The repository source inventory at `Docs/researches/math_theorems.md:6376-6381` contains exactly:

| Field | Repository wording | Intake interpretation |
|---|---|---|
| title | `树宽` | Treewidth topic/invariant name; not a proposition |
| attribution | `Neil Robertson/Paul Seymour` | Unreviewed catalog attribution |
| time | `1984` | Unreviewed catalog date |
| statement | `图的树分解` | "Tree decompositions of graphs"; no binders, assumptions, or conclusion |
| importance | `高` | Scheduling metadata only |
| formalization status | `已验证` | Explicitly untrusted; no H or M credit |

All six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The Stage0 projection at
`Docs/Stage0_Blueprint.md:23738-23763` repeats the label and gloss, but marks exact definitions,
premises, proof history, equivalent statements, axioms, machine status, and artifact links as
missing. Neither surface supplies an exact theorem.

## Bibliographic lead

Crossref metadata was inspected for Neil Robertson and P. D. Seymour, *Graph minors. II.
Algorithmic aspects of tree-width*, Journal of Algorithms 7(3) (1986), 309-322, DOI
`10.1016/0196-6774(86)90023-4`. It confirms the article identity and records related Graph Minors
references, including *Graph minors. III. Planar tree-width* (1984) and a then-submitted
*Graph minors. IV. Tree-width and well-quasi-ordering*. This metadata does not identify which
definition or theorem the catalog intended, and the full primary text, exact locator,
incorporated definitions, assumptions, proof, correction history, and independent review were not
admitted. It is a discovery lead only, not H0 or a canonical-root decision.

## Source-to-statement gaps

| Required element | Current status |
|---|---|
| one truth-valued canonical claim | absent; title and gloss name a family |
| graph and tree-index domains | absent |
| bag representation and finiteness | absent |
| vertex, edge, and running-intersection conditions | absent |
| width/treewidth convention and attainment | absent |
| ordered binders, hypotheses, conclusion | absent |
| degenerate and boundary cases | absent |
| primary edition and exact definition/theorem/page | absent |
| assumption, proof-boundary, correction, and errata map | absent |
| independent source reviewer | unassigned |
| exact Lean expression and checked transports | absent |

The provisional `H5` therefore classifies the received wording as not yet a stable proposition. It
does not refute, contest, or declare open any standard theorem about treewidth.

## Formal crosswalk boundary

The pinned Lean probe checks only `SimpleGraph`, adjacency, `IsTree`, induced graphs, tree
invariance under graph isomorphism, spanning-tree existence, and finite-set cardinality. None
defines tree decompositions, decomposition width, treewidth, bounded treewidth, or a selected
theorem. No formal declaration or proof body is credited. The statement gate must first select and
source-review one exact root, then elaborate an identical Lean expression with minimal imports,
fingerprints, checked transports, and required mutations.

## Admission gate

Source admission requires a lawfully preserved authoritative edition, stable pinpoint locator,
incorporated definitions, complete premise/conclusion/proof-boundary crosswalk, corrections and
errata disposition, neighbor-target reconciliation, and independent graph-theory review. Until
then, the catalog, bibliographic metadata, and formal substrate remain discovery evidence only.
