# Scope map

## Preserved theorem family

The intake preserves the conventional Four Color Theorem family:

- a finite simple graph with a source-approved notion of planar embedding is properly colorable
  with at most four colors; or
- the regions of a source-defined simple planar map can be assigned at most four colors so that
  adjacent regions receive different colors;
- graph and map formulations are interchangeable only after a checked representation theorem maps
  vertices/faces, adjacency, simplicity, finiteness, and planarity in both required directions.

The graph conclusion has a natural pinned Lean candidate, `G.Colorable 4`, meaning
`Nonempty (G.Coloring (Fin 4))`. That observation does not select the graph premise or freeze a
canonical target.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved immutable source:

1. Graph coloring versus planar-map region coloring as the canonical root, and every credited
   graph-map transport.
2. A finite graph as a `Fintype` carrier, a `Finite` carrier, a finite edge set, a finite embedding,
   or another source-defined notion.
3. Planarity via an embedding into the plane or sphere, a rotation system/combinatorial map, a
   hypermap satisfying an Euler condition, excluded minors, or another equivalent predicate.
4. Simple undirected graphs versus multigraphs, loops, bridges, disconnected graphs, isolated
   vertices, repeated edges, and whether simplicity is a type-level invariant or a premise.
5. Whether `four colors` means a map to exactly `Fin 4`, use of at most four colors, or chromatic
   number at most four; unused colors must be allowed for the usual theorem.
6. For planar maps, the exact carrier of regions; openness, connectedness and pairwise-disjointness;
   the real-plane model; closures; corners; and the adjacency rule.
7. Empty graphs/maps, zero through four vertices, edgeless and disconnected graphs, bridge edges,
   empty/unbounded regions, touching only at a point, and other degenerate embeddings.
8. Universe levels, decidable equality, finite instances, classical choice, real-number axioms,
   computation/certificate policy, and ordered binder/typeclass scope.

## Explicit exclusions

- The Five Color Theorem, a bound of five or more colors, or a result only for triangulations,
  cubic graphs, bridgeless graphs, hypermaps, connected graphs, or one fixed planar graph cannot
  replace the general root without checked reductions.
- `Colorable 4` may not be assumed as a structure field or hypothesis and then projected.
- A topological map theorem may not be silently replaced by a graph theorem, or vice versa, without
  checked representation and adjacency transports.
- The existence of a Rocq/Coq proof does not establish a Lean 4 theorem, and an external URL or
  immutable commit is not repo-local proof closure.
- `SimpleGraph.colorable_of_fintype` proves only a bound by the number of vertices; it is not the
  Four Color Theorem.
- A finite computation, drawing, coloring heuristic, SAT result without a checked soundness bridge,
  or testing sample is not a universal proof.
- The neighboring records `THM-M-0836`, `THM-M-0837`, and `THM-M-0838` describe proof methods or
  formalization projects; their wording and status do not alter this target's root.
- The catalog label `已验证` is not source, kernel, or completion evidence.

## Intake boundary

This intake freezes the family, ambiguity ledger, source leads, non-substitution rules, and workflow.
It deliberately leaves the canonical Lean expression, expression fingerprint, checked transports,
mutation tests, exhaustive anchor audit, proof-body provenance, obligation registry, typed graphs,
and proof work to their assigned downstream phases.

