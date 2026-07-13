# Scope map

## Preserved theorem family

The intake preserves Vizing's finite edge-coloring theorem family. The inspected reference source
gives the loopless-multigraph inequality
`Delta(G) <= chi'(G) <= Delta(G) + mu(G)`, where `mu(G)` is maximum parallel-edge multiplicity, and
then the finite-simple-graph specialization `Delta(G) <= chi'(G) <= Delta(G) + 1`.

The repository gloss does not choose between those two scopes. Mathlib's `SimpleGraph` represents
only the simple specialization. Selecting it without accepted source review would silently discard
the parallel-edge case; inventing a multigraph encoding would likewise settle an unstated choice.
The statement phase must choose the exact source-backed proposition and record any separately
checked specialization or transport.

## Decisions required at statement freeze

1. Whether the canonical root is the loopless-multigraph theorem or the finite-simple-graph
   specialization, and why that is the proposition intended by the catalog record.
2. The graph representation, vertex and edge universes, finiteness hypotheses, treatment of
   parallel edges, exclusion of loops, and decidability/typeclass boundary.
3. Whether chromatic index is defined directly as the least size of a proper edge-color palette or
   transported through vertex coloring of the line graph.
4. The exact meaning of adjacent edges and proper edge coloring, including distinct parallel edges
   and edges that share either endpoint.
5. The definitions and codomains of maximum degree, maximum multiplicity, and chromatic index, plus
   every `Nat`/`ENat` coercion if numerical minima rather than `Colorable` are used.
6. Whether the lower bound is part of the root or a separately composed elementary obligation, and
   whether the upper bound is expressed as an inequality or existence of a coloring.
7. The exact ordered binders, typeclasses, minimal imports, alternate-encoding transports,
   foundation/TCB/computation profiles, and statement mutations required by rev-5.6.

## Degenerate and boundary cases

Source review and mutation tests must address the empty vertex type, an edgeless nonempty graph,
one edge, matchings, paths, cycles of odd and even length, complete graphs, stars, disconnected
graphs, isolated vertices, maximum degree zero, and graphs attaining either `Delta` or `Delta + 1`.
If the multigraph form is selected, they must additionally address parallel edges, multiplicity
zero or one, a two-vertex bundle of parallel edges, and why loops are excluded. Typeclass choices
must not become unintended mathematical hypotheses.

## Excluded substitutions

- Shannon's multigraph bound, `THM-M-0860`, has the different upper bound `3 Delta / 2`.
- Konig's edge-coloring theorem, `THM-M-0861`, gives equality only for bipartite graphs.
- Brooks' theorem, `THM-M-0858`, bounds vertex chromatic number, not edge chromatic number.
- Vizing's total-coloring conjecture, list-edge-coloring conjecture, planar class-one theorem, and
  adjacency lemma are different claims.
- A lower bound alone, only one graph class, only finite experiments, or an assumed coloring object
  is not Vizing's theorem.
- A theorem about arbitrary vertex coloring, an unproved equivalence slogan, or the catalog label
  `已验证` supplies no source or kernel credit.

## Formal boundary

For a finite simple graph, a prospective encoding is
`G.lineGraph.Colorable (G.maxDegree + 1)`: line-graph vertices are edges of `G`, adjacency means
distinct edges sharing a vertex, and a line-graph coloring is a proper edge coloring. This exact
expression is not the canonical statement at intake. The statement phase must source-approve the
simple specialization, freeze finite/decidable instances, check the direct-edge-coloring transport,
and verify all boundary cases before fingerprinting it. The multigraph theorem needs a different
representation not supplied by `SimpleGraph`.
