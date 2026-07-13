# Scope map

## Preserved theorem family

The intake preserves the graph-theoretic Wagner theorem indicated by the catalog attribution, year,
and forbidden-minor gloss. Its familiar modern candidate is:

> A finite graph is planar if and only if it has neither `K5` nor `K3,3` as a graph minor.

This is a candidate scope discriminator, not the frozen canonical proposition. A proposition-level
primary source, exact definitions, and independent review are absent. The statement phase must not
silently replace the catalog by the familiar wording or inspect proof closure before the exact
source-to-Lean mapping is accepted.

## Decisions required at statement freeze

1. Select and preserve an immutable proposition-level source, pinpoint the theorem and every
   incorporated definition, map its hypotheses and conclusion, inspect corrections and errata,
   and obtain independent review.
2. Fix the graph class: finite simple graphs, finite multigraphs, one-dimensional complexes, or an
   explicitly transported modern encoding. Loops, parallel edges, isolated vertices, and carrier
   finiteness cannot be changed by convention.
3. Define abstract graph planarity, including the embedding target and equivalence with any
   source-era notion of a "plane complex." Plane drawings or embeddings supplied as hypotheses do
   not characterize graphs that admit such embeddings.
4. Define the graph-minor relation and its orientation using explicit deletion and edge-contraction
   witnesses. Ordinary subgraph, induced subgraph, topological minor, and matroid minor relations
   are noninterchangeable.
5. Fix exact `K5` and `K3,3` encodings, including whether they use `completeGraph (Fin 5)` and
   `completeBipartiteGraph (Fin 3) (Fin 3)`, and compile checked transports for alternatives.
6. Decide whether the root is an `Iff`, a no-forbidden-minor implication plus its converse, or a
   source-equivalent formulation connected by checked witnesses.
7. Freeze universes, ordered binders, typeclasses, all hypotheses and conclusion, minimal imports,
   foundation/TCB/computation profiles, and the elaborated expression/environment fingerprints.
8. Mutation-test finiteness, graph model, minor orientation, both obstructions, binder scope, and
   boundary cases before proof evidence is inspected.

## Boundary cases

No case is excluded at intake. Statement work must decide empty and singleton graphs, isolated
vertices, edgeless and disconnected graphs, graphs with fewer than five vertices, loops and
parallel edges if the source admits them, deletion to an empty graph, contraction of bridges and
parallel-edge cleanup, and whether vertex deletion is primitive or encoded through other minor
operations.

## Neighbor and substitution boundaries

- `THM-M-0865` is Kuratowski's forbidden-subdivision/topological-subgraph characterization. It is
  not Wagner's forbidden graph-minor characterization, even though the theorems are related.
- `THM-M-0867` and `THM-M-0868` concern the Robertson-Seymour graph-minor well-quasi-order theorem
  and the broader graph-minor theorem family. Their statements and proof credit do not transfer.
- A one-direction statement, only the `K5` obstruction, only the `K3,3` obstruction, a planar edge
  bound, or a fixed finite-graph computation cannot replace the biconditional root.
- A hypothesis or structure that stores planarity or forbidden-minor absence cannot serve as the
  proof, and the catalog's untrusted `已验证` label supplies no source or machine credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Basic` defines `completeGraph` and
`completeBipartiteGraph`; `SimpleGraph.Copy` and `SimpleGraph.Maps` provide subgraph-copy,
induced-graph, and embedding substrate. The intake probe checks adjacent completed interfaces only.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found no graph-minor,
planarity, Kuratowski-planarity, or Wagner declaration. The sole planar-graph occurrence in the
pinned SimpleGraph tree is a TODO bullet in `Coloring.lean`. Matroid minor APIs elsewhere in
mathlib concern a different object and relation. These observations are intake reconnaissance, not
an exhaustive external anchor audit or a global absence proof.
