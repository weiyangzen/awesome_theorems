# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6341-6346` supplies exactly `Kuratowski定理`, Kazimierz
Kuratowski, 1930, the gloss `平面图的禁用子图刻画`, importance `高`, and status `已验证`. All six
uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, graph convention,
definitions, quantifiers, hypotheses, conclusion, bibliography, theorem/page locator, proof,
correction history, formal declaration, or reviewer.

`Docs/Stage0_Blueprint.md:23603-23628` projects this record while explicitly leaving the exact
definitions and premises, proof route, dependencies, equivalent forms, foundations, axioms,
machine status, and artifact links open. Rev-5.6 therefore retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Historical primary-source lead

Crossref identifies Casimir Kuratowski, "Sur le probleme des courbes gauches en Topologie,"
*Fundamenta Mathematicae* 15 (1930), pages 271-283, DOI
`10.4064/fm-15-1-271-283`. This matches the catalog attribution and year and is the historical
primary-source lead. The article text, its exact theorem locator and vocabulary, incorporated
definitions, scope, assumptions, proof nodes, corrections and errata were not admitted or reviewed
in this intake. The DOI metadata is a bibliographic discriminator, not H0 evidence.

## Inspected modern source lead

Reinhard Diestel, *Graph Theory*, 6th edition (2025), author-hosted Chapter 4, Section 4.4,
"Planar graphs: Kuratowski's theorem," was inspected as a modern authoritative source lead. The
observed 30-page chapter PDF has SHA-256
`bfdfbcb1e7c0df0d6fc1322ae02b11a8c7ef5c6c85f509e96ad20ad7665b15a9`.
Printed page 107 says the aim is the converse that every graph without a topological `K5` or
`K3,3` minor is planar. Theorem 4.4.6 on printed page 111 states that, for graphs `G`, these are
equivalent: `G` is planar; it contains neither `K5` nor `K3,3` as a minor; it contains neither as a
topological minor.

Diestel's author-hosted Chapter 1 was also inspected; its observed PDF has SHA-256
`ebd9084653a1a534b964cbe327eeb8ab6b46a5e98deeee94280b05ebb6f37b56`. Section 1.1 on printed
page 2 fixes the book's ordinary graph convention as finite, simple, and undirected outside
Chapter 8 unless stated otherwise. Section 1.7 on printed pages 18-19 defines a subdivision by
replacing source edges with paths whose inner vertices are neither original branch vertices nor
shared with another replacement path, and defines `X` as a topological minor of `Y` when `Y`
contains such a subdivision as a subgraph. Thus the inspected Diestel candidate has finite-simple
scope; whether the uncited catalog and historical source select that exact scope remains open.

This supports provisional H1, not H0. The source is a modern presentation rather than the admitted
1930 edition; Theorem 4.4.6 combines Kuratowski 1930 with Wagner 1937; no complete premise-to-proof-
node crosswalk, corrections audit, or independent review has been accepted.

## Clause crosswalk

| Catalog/source clause | Exact modern-source role | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| planar graph | abstract graph isomorphic to a graph embedded in the plane | approved `Planar G` definition or embedding-existence predicate | absent from pinned mathlib; representation open |
| forbidden subgraphs | subdivisions of `K5` and `K3,3` occur as non-induced subgraphs | source-defined subdivision plus subgraph/isomorphism witness | catalog phrase is ambiguous; literal subgraph exclusion rejected |
| topological minor | host contains a subdivision of the source graph | future `IsTopologicalMinor X G` or checked path-model encoding | no pinned interface located |
| subdivision | each source edge is replaced by an internally disjoint path | branch embedding and edge-path family with incidence/disjointness proofs | no pinned interface located |
| `K5` | complete graph on five vertices | `SimpleGraph.completeGraph (Fin 5)` | adjacent pinned graph authenticated only |
| `K3,3` | complete bipartite graph with two three-vertex parts | `SimpleGraph.completeBipartiteGraph (Fin 3) (Fin 3)` | adjacent pinned graph authenticated only |
| iff characterization | planarity is both necessary and sufficient for absence of both obstructions | one exact `Iff`, or checked paired implications | binder and encoding not frozen |
| ordinary minor clause | Diestel's equivalent clause, jointly Kuratowski/Wagner | future minor-model predicate and checked transport | neighbor `THM-M-0866`; not selected here |
| `已验证` | untrusted inventory status | accepted source/kernel receipts would be required | no H/M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, pinned modules define
`SimpleGraph`, `SimpleGraph.Iso`, `SimpleGraph.Copy`, `SimpleGraph.IsContained`,
`SimpleGraph.completeGraph`, and `SimpleGraph.completeBipartiteGraph`. The intake probe elaborates
these adjacent interfaces and a predicate-parameterized theorem shape only.

A bounded case-insensitive search over repo-local Lean and pinned `Mathlib/Combinatorics/SimpleGraph`
found no Kuratowski, graph-planarity, subdivision, topological-minor, or ordinary graph-minor
declaration. This is narrow reconnaissance, not an exhaustive anchor audit or a global absence
claim. No target-specific declaration, source-faithful definition, proof body, or M1/M0 state is
credited.

## First blocker and retry condition

An independent graph-theory source reviewer must select the exact Kuratowski root and admit an
immutable source version, fixing finite/general and simple/multigraph scope, planarity, subdivision,
topological-minor containment, obstruction encodings, ordered binders, assumptions, conclusion,
foundations, corrections, degenerate cases, and the ownership boundary with Wagner's theorem. Only
then may statement work elaborate the reviewed target with minimal pinned imports, serialize its
expression and environment fingerprints, add checked alternate transports, and run all required
mutations.
