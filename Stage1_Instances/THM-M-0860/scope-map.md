# Scope map

## Preserved theorem family

The intake preserves target `THM-M-0860`, the title `Shannon定理`, Claude Shannon, the year 1949,
and the graph-theoretic gloss `边色数的上界`. Together with the matching 1949 article title, these
identify the Shannon multigraph edge-colouring upper-bound family. The catalog importance and
`已验证` status remain untrusted metadata.

The standard modern candidate is:

```text
for every finite loopless multigraph G,
chromaticIndex(G) <= floor (3 * maximumDegree(G) / 2).
```

Equivalently, one expects a proper edge-colouring with at most `floor (3 * Delta / 2)` colours.
This text records a source-resolution candidate only. It is not an adopted canonical proposition,
an elaborated Lean target, or proof evidence.

## Decisions required at statement freeze

An immutable, independently reviewed source must settle all of the following before exact Lean
elaboration:

1. Whether the source domain is a finite multigraph, a finite edge set on a possibly ambient vertex
   type, or another network model, and the exact universe and finiteness assumptions.
2. Whether loops are prohibited. Under the usual proper edge-colouring convention a loop conflicts
   with itself, so allowing loops can make the target false or require a changed definition.
3. How parallel edges are represented and distinguished. They are essential target data, not an
   encoding nuisance that may be collapsed to a simple graph.
4. The degree convention, especially how incident parallel edges and any allowed loops contribute,
   how maximum degree is obtained, and how the empty graph is treated.
5. Whether a proper edge-colouring assigns a colour to every edge and requires distinct colours for
   every pair of distinct incident edges, and how the chromatic index is the least palette size.
6. The exact arithmetic form of the bound: `floor (3 * Delta / 2)`, natural-number division
   `(3 * Delta) / 2`, or an equivalent ceiling form with a checked transport.
7. Whether the root states only the upper bound, an existence theorem, the inequality together with
   a lower bound, or also sharpness and a three-vertex extremal family.
8. Ordered binders, typeclasses, foundation/TCB/computation profiles, minimal imports, exact source
   definitions, correction state, and all statement mutations required by rev-5.6.

## Boundary and degenerate cases

No case is excluded at intake. Source review must decide empty vertex and edge sets, edgeless
graphs, isolated vertices, one-edge graphs, maximum degrees `0` and `1`, two vertices with parallel
edges, three-vertex extremal multigraphs for even and odd degree, disconnected graphs, infinite
ambient carrier types with finite graph support, and any loop-containing input. It must also check
that palette cardinality and natural-number division give the intended bound in every low-degree
case.

## Excluded substitutions

- `THM-M-0858` Brooks' theorem bounds vertex chromatic number; it is not edge colouring.
- `THM-M-0859` Vizing's theorem concerns the simple-graph edge-colouring bound and cannot replace
  the parallel-edge Shannon theorem.
- `THM-M-0861` Konig's edge-colouring theorem gives equality with maximum degree for bipartite
  graphs, a stronger conclusion on a narrower domain.
- A simple-graph line-graph coloring loses distinct parallel edges unless an explicit, checked
  faithful encoding is supplied.
- An arbitrary `SimpleGraph.EdgeLabeling` is not a proper edge-colouring without the incidence
  separation condition and a complete palette-size statement.
- A result assuming the desired colouring, chromatic-index inequality, or decomposition as a field
  or hypothesis is not Shannon's theorem.
- A finite enumeration or algorithm run without a general checked correctness proof cannot close
  the theorem.
- The catalog's `已验证` label, article title, DOI, API `#check`, or bounded no-match search provides
  no H0 or machine-proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Graph` supplies explicit
vertex and edge sets, link incidence, loops, nonloops, adjacency, and parallel-edge identity.
`Graph.IsSubgraph` supplies an explicit-edge subgraph relation. Adjacent `SimpleGraph` APIs supply
edge labelings plus simple-graph degree and maximum degree. The pinned `Graph` directory has no
located degree, maximum-degree, proper edge-colouring, or chromatic-index layer, and the bounded
exact-topic search found no target theorem. These are intake feasibility observations, not an
exhaustive formal-candidate audit or a proof of external absence.
