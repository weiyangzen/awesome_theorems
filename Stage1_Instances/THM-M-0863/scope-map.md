# Scope map

## Preserved theorem family

The intake first preserves Whitney's historical theorem: a non-separable graph containing at least
two arcs can be built from a circuit by successively adding arcs or suspended chains while each
partial graph remains non-separable, and a graph built this way is non-separable. The catalog's
short wording apparently maps that result to the modern 2-connected/open-ear theorem family, but
that mapping is not yet accepted.

This is a source-backed family description, not a frozen canonical proposition. Whitney's own
Theorem 19 uses a finite, multigraph-like historical graph with separately named arcs and calls each
new piece either an arc or a suspended chain; the next sentence states the converse. The catalog's
short modern gloss does not say whether the root is the construction direction, the converse, or
the biconditional. The statement phase must independently approve one exact source interpretation
before it may create an elaborated expression fingerprint.

## Decisions required at statement freeze

1. Fix the graph model. Whitney's graph permits loops and parallel arcs, while mathlib's
   `SimpleGraph` forbids both. A modern simple-graph theorem needs an explicit, checked source
   transport rather than silently treating the models as identical.
2. Fix the connectivity predicate. Whitney's non-separable graphs include single-arc cases and are
   defined through decomposition at a vertex. Modern "2-connected" may instead require at least
   three vertices and connectedness after deleting any one vertex, or use two internally
   vertex-disjoint paths. These formulations need hypotheses and checked equivalences.
3. Fix the base object: a cycle subgraph, a cyclic walk, or a graph isomorphic to a cycle; determine
   whether Whitney's 1- and 2-circuits disappear in the simple-graph specialization.
4. Define an ear exactly: an open path whose endpoints lie in the prior subgraph and whose internal
   vertices do not, whether a single edge is an ear, whether endpoints must be distinct, and whether
   every ear edge is new and the final union equals the ambient graph.
5. Fix the decomposition carrier and order: a finite list/vector of subgraphs or paths, its initial
   cycle, partial unions, attachment invariant, coverage invariant, and possible empty tail.
6. Decide whether the root asserts existence from 2-connectivity, preservation of 2-connectivity,
   the converse, or a biconditional. None may be substituted for another without source approval.
7. Fix finite vertex and edge assumptions, universes, decidability, ordered binders, foundation and
   TCB profiles, minimal imports, checked alternate encodings, and all rev-5.6 statement mutations.

## Degenerate and boundary cases

Statement review must explicitly address empty and singleton graphs, one edge, paths, triangles,
cycles of length three and four, complete and edgeless graphs, disconnected graphs, graphs with a
cut vertex, a final graph equal to the initial cycle, single-edge ears, ears of path length two,
coincident endpoints, repeated internal vertices, unused ambient vertices, isolated vertices, and
the loop/parallel-edge cases present in Whitney's model but absent from `SimpleGraph`.

## Excluded substitutions

- Whitney's line-graph isomorphism theorem, Whitney embedding theorem, and Whitney approximation
  theorem are different results sharing an author name.
- Menger's theorem (`THM-M-0862`) and Tutte connectivity theorem (`THM-M-0864`) may provide future
  dependencies but do not state an ear decomposition.
- An edge-connectivity ear theorem, directed strong-connectivity ear theorem, matroid ear theorem,
  convex ear decomposition, or an ear result only for special graph classes is not this target.
- Merely proving that adding one path preserves ordinary connectedness is weaker than the source
  family and does not provide a complete decomposition.
- A structure whose fields assume 2-connectivity, attachment, or coverage cannot stand in for the
  existence theorem.
- A title, source URL, `#check`, or the untrusted catalog label `已验证` supplies no H or M credit.

## Neighbor boundaries

`THM-M-0862` owns Menger's disjoint-path theorem and `THM-M-0864` owns Tutte's connectivity
theorem. Graph connectivity and path APIs may become shared substrate only after exact dependency
freezes; no neighboring target grants proof status here.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks ordinary connectivity,
paths and cycles, induced subgraphs, vertex deletion, and walk-to-subgraph conversion. A bounded
source search found no exact ear-decomposition or named vertex-2-connectivity declaration. This is
scoped discovery evidence, not the exhaustive anchor audit and not a proof of global absence.
