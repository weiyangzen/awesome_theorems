# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6005-6010` supplies the name Ramsey's theorem, attribution Frank
Ramsey, year 1930, and the complete gloss `任意大的图中必有大的完全子图或独立集` (arbitrarily large
graphs contain large complete subgraphs or independent sets). Git history places all six uncited
lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no parameter
binders, graph model, finite/infinite choice, threshold, cardinal convention, proof boundary,
bibliography, or formal declaration.

`Docs/Stage0_Blueprint.md:22307-22332` repeats the gloss while leaving exact definitions and
premises, proof route, dependency graph, alternate formulations, axioms, machine state, and
artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

## Source leads

Crossref DOI metadata identifies F. P. Ramsey, *On a Problem of Formal Logic*, *Proceedings of the
London Mathematical Society* s2-30(1), 264-286 (1930), DOI
`10.1112/plms/s2-30.1.264`. This matches the catalog's author and year, but only metadata was
observed: the source article, exact result passage, incorporated definitions, assumptions, proof
boundary, and corrections were not inspected.

The inspected statement-bearing secondary lead is Diana Bergerova, *Game of SIM and Ramsey
theory*, *Rozhledy matematicko-fyzikalni* 97(4) (2022), 13-18, DML-CZ persistent handle
`10338.dmlcz/151634`, observed PDF SHA-256
`cff253253e87f944092bbbb26f328ce8e330b3e07369750b0c4695ba1fad0e86`. Printed page 14
states that for all `k,r` there exists `n` such that every `k`-coloring of the edges of `K_n` has
an `r`-vertex monochromatic complete subgraph. Printed pages 15-16 separately define `R(r,b)` as
the least vertex count forcing a red `r`-clique or blue `b`-clique. The article says Ramsey's 1930
paper proved finite and infinite versions and cites it at pages 264-286.

This secondary source confirms the family and exhibits the finite general-color and asymmetric
two-color variants; it does not select which one the catalog means. It is not the catalog-cited or
primary proof source, and no complete source-to-node map, correction audit, or independent review
has been accepted. It supports provisional `H1`, not `H0`.

## Component crosswalk

| Catalog/source component | Candidate mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| graph | finite simple graph on a sufficiently large carrier | `SimpleGraph alpha` | carrier, finiteness, and cardinal encoding open |
| complete subgraph | pairwise adjacent vertex set of requested size | `G.IsClique s`; `G.IsNClique r s` | vocabulary match only |
| independent set | pairwise nonadjacent vertex set of requested size | `G.IsIndepSet s`; `G.IsNIndepSet s s` | vocabulary match only |
| graph/complement encoding | one edge color is adjacency and the other is nonadjacency | `isClique_compl`; `isIndepSet_compl`; finite-cardinality analogues | useful transport ingredients; no Ramsey conclusion |
| "large" homogeneous set | exactly or at least `r` vertices; symmetric or separate sizes | finite-cardinality predicates exist | parameter and cardinal convention absent |
| "arbitrarily large" graph | `forall r, exists N, forall G` with a lower-bound/cardinality condition | no canonical expression selected | quantifier order and threshold model absent |
| general `k`-edge-coloring | monochromatic `r`-set in a complete graph | no matching terminal declaration located | credible source variant, not selected root |
| least Ramsey number | minimal threshold `R(r,s)` | no selected definition or declaration | strictly stronger packaging than bare existence |
| `已验证` | untrusted catalog status | no proof object or receipt | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Clique` supplies clique, exact-cardinality clique,
independent-set, exact-cardinality independent-set, and complement equivalences.
`IntakeProbe.lean` elaborates those APIs against the pinned environment.

A bounded case-insensitive search for `Ramsey` in repo-local Lean and pinned mathlib found only an
unrelated contributor surname and prose describing Hales-Jewett and Hindman as Ramsey theory. No
combinatorial Ramsey terminal declaration was identified. That bounded observation is not proof of
absence and is not the downstream anchor audit. With no exact statement or usable exact formal
artifact, the provisional machine status is `M4`.

Before leaving `H1`, accountable reviewers must preserve and hash a lawful primary edition,
pinpoint and transcribe the exact result, map every definition, parameter, hypothesis, conclusion,
and proof boundary, audit corrections, and approve its identity with THM-M-0817. Before machine
credit, the statement phase must freeze and mutation-test the exact elaborated target and every
credited transport.
