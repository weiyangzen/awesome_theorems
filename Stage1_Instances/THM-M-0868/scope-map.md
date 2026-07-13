# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0868`, the title `图子式定理`, attribution Robertson/Seymour,
the period 1983-2004, and the gloss `Wagner猜想的证明`. Bibliographic discovery identifies the
likely source family as Robertson and Seymour's 2004 Graph Minors XX result. A secondary abstract
gives this prospective mathematical shape:

```text
Every infinite collection of finite graphs contains two distinct members such that one is
isomorphic to a minor of the other.
```

This is a source-family discriminator, not the canonical statement. The primary theorem passage
and incorporated definitions were not inspected or accepted, and the catalog may duplicate
`THM-M-0867` rather than define an independent root.

## Proposition-changing decisions

An exact source and independent review must determine:

1. Whether graphs are finite undirected simple graphs, finite multigraphs, or another source model;
   and how loops, parallel edges, isolated vertices, and graph equality are treated.
2. Whether the quantified collection is a set, a sequence indexed by natural numbers, or a class
   of isomorphism types, including how duplicates and countability are handled.
3. Whether the conclusion uses literal graph equality, graph isomorphism, or equivalence classes
   modulo isomorphism.
4. The exact minor relation: a sequence of vertex deletion, edge deletion, and edge contraction;
   an equivalent branch-set/minor-model predicate; or another source definition.
5. Edge-contraction semantics, especially loops and parallel edges created by contraction and any
   simplification back to simple graphs.
6. The direction and argument order of the minor relation and the order of the witness indices.
7. Whether the root is the infinite-set formulation, the natural-sequence WQO formulation
   `WellQuasiOrdered minor`, a monotone-subsequence form, or a checked transport among them.
8. Ordered binders, universes, finiteness witnesses, decidability/typeclass inputs, foundation and
   trust profiles, minimal imports, and all rev-5.6 statement mutations.

## Boundary cases

- the empty graph, edgeless graphs, and graphs with zero or one vertex;
- repeated isomorphic graphs in a sequence or collection;
- finite collections presented through an infinite sequence with repetition;
- deletion of all vertices or edges and contraction of bridges, loops, or parallel edges;
- a graph treated as its own minor and the distinction between minor and proper minor;
- fixed ambient vertex types versus graphs whose vertex types vary;
- labelled, rooted, directed, embedded, infinite, hypergraph, and matroid variants; and
- set-level choice used to enumerate an infinite collection or choose graph representatives.

No case is silently excluded before the exact proposition is source-approved.

## Excluded substitutions

- A theorem only about subgraphs, induced subgraphs, edge deletion, or vertex deletion; contraction
  is essential to the graph-minor relation.
- Kruskal's tree theorem, Higman's lemma, Dickson's lemma, or a generic WQO theorem used as the
  graph-specific root.
- The matroid minor order, graph immersion, topological minor, induced minor, subdivision, or
  homomorphic image used as an ordinary graph minor without a checked equivalence.
- Wagner's planar-graph characterization, `THM-M-0866`, or a finite forbidden-minor corollary used
  as the full well-quasi-order theorem.
- A labelled, rooted, bounded-treewidth, planar-only, finite-enumeration, or fixed-size special case.
- A structure or premise that stores the requested WQO theorem or minor witness as input.
- The catalog's `已验证` label, a paper title, abstract, DOI, API probe, or bounded negative search
  used as human-proof or machine-proof closure.

## Neighbor and duplicate boundary

`THM-M-0867` is separately scheduled with the title `Robertson-Seymour图子式定理` and gloss
`图子式良拟序定理`. Those words and the shared authors strongly suggest the same Graph Minor
Theorem family. This is duplicate evidence, not an accepted identity decision. Until the integration
lane decides canonical ownership and exact-statement identity, both targets remain independent L0
instances and share no receipt, source, obligation, proof body, or status.

`THM-M-0866` is Wagner's planar-graph forbidden-minor characterization. It is a distinct theorem.
`THM-M-0869` concerns forbidden-subgraph problems generally and cannot supply this root.

## Lean boundary

Pinned mathlib supplies `SimpleGraph`, `SimpleGraph.deleteEdges`,
`SimpleGraph.Subgraph.deleteVerts`, `SimpleGraph.Iso`, `SimpleGraph.induce`, and
`WellQuasiOrdered`. It does not supply a located `SimpleGraph` contraction/minor relation or the
Robertson-Seymour theorem. The discovery probe only authenticates adjacent interfaces. Exact graph
encoding, minor relation, isomorphism quotient, WQO transport, target expression, fingerprints,
mutations, and proof provenance remain downstream work.
