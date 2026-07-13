# Scope map

## Preserved theorem family

The received phrase "characterization of planar graphs by forbidden subgraphs" is preserved as the
Kuratowski theorem family, not expanded into an accepted exact statement. The standard modern
candidate is:

- an abstract graph is planar if and only if it contains neither `K5` nor `K3,3` as a topological
  minor; equivalently, it contains no subgraph isomorphic to a subdivision of either graph.

Diestel's Theorem 4.4.6 additionally gives absence of `K5` and `K3,3` as ordinary minors. The
ordinary-minor clause is jointly attributed to Wagner and belongs to neighboring target
`THM-M-0866`; it is an alternate candidate only after an explicit ownership and checked-transport
decision. A literal ordinary subgraph exclusion is too weak and is not a valid substitute for
subdivision/topological-minor exclusion.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved immutable source:

1. Whether the canonical root uses subdivisions, topological minors, or a reviewed equivalence;
   whether the ordinary-minor form is excluded, shared, or admitted only as a checked alternate.
2. Finite graphs only or the source's broader graph convention, and every local finiteness or
   cardinality condition needed by the chosen formulation.
3. Simple undirected graphs versus multigraphs, including loops, parallel edges, and how their
   erasure or encoding interacts with planarity and containment.
4. Abstract planarity as existence of an isomorphic plane graph versus explicit plane/sphere
   embeddings, including vertices, edge arcs, crossings, touching, and topological regularity.
5. A subdivision as replacement of every source edge by internally vertex-disjoint paths, with
   exact branch-vertex, path-length, incidence, and unused-host-vertex conditions.
6. Topological-minor containment as a subdivision subgraph or an edge-to-independent-path
   embedding, and the checked equivalence between those encodings.
7. Exact Lean representations of `K5` and `K3,3`, their vertex types, graph isomorphism, subgraph
   containment, and whether containment is induced or non-induced.
8. Ordered binders, universes, typeclass assumptions, decidability, classical choice, topology,
   quotient, and computation policies.

## Boundary cases

No case is excluded at intake. Statement work must settle empty and singleton graphs, edgeless
graphs, forests, disconnected graphs, isolated vertices, bridges, graphs of fewer than five or six
vertices, pre-existing degree-two vertices, unsubdivided edges, paths of positive length, and
multiple embeddings or models. It must also specify loops and parallel edges if the source graph
model permits them.

## Explicit exclusions

- Wagner's ordinary-minor characterization (`THM-M-0866`) cannot silently replace or duplicate the
  Kuratowski topological-minor/subdivision root.
- A claim that merely forbids literal copies of `K5` and `K3,3` as ordinary subgraphs is not the
  theorem: subdivisions can be nonplanar without containing either unsubdivided graph.
- The Four Color Theorem (`THM-M-0833`), Euler's planar formula (`THM-M-0810`), a planarity
  algorithm, or any one-way necessary condition cannot replace the bidirectional characterization.
- A `Planar`, `Subdivision`, or `IsTopologicalMinor` predicate supplied as a parameter or structure
  field cannot be treated as a source-faithful definition or proof.
- A desired equivalence stored as a hypothesis, a fixed finite example, drawing, search result, or
  decision procedure without a checked soundness/completeness bridge supplies no theorem credit.
- The untrusted `已验证` label, theorem name, DOI, secondary summary, or successful API probe is not
  human-source or kernel evidence.

## Intake boundary

This intake freezes the received family, source leads, ambiguity ledger, exclusions, neighbor
ownership, and open workflow. The exact mathematical and Lean statement, checked alternate
encodings, expression/environment fingerprints, statement mutations, exhaustive anchor audit,
obligation registry, typed graphs, proof, and release evidence remain downstream.
