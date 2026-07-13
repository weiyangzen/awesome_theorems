# THM-M-0861 scope map

## Preserved theorem family

The intake preserves the finite bipartite multigraph theorem identified jointly by the catalog and
König's 1916 Satz C: a graph of maximum degree `Delta` admits a proper edge coloring
with `Delta` colors, hence its edge chromatic number equals `Delta` after the elementary lower
bound. Parallel edges are part of the historical source and are not silently discarded.

This is a source-backed family description, not a frozen Lean proposition. The statement phase
must independently approve an exact encoding before it creates an elaborated expression or
examines proof closure.

## Decisions required at statement freeze

1. A finite multigraph representation with edge identity and incidence, including parallel edges,
   vertex and edge universes, finiteness witnesses, decidable equality needs, and a reviewed
   decision that the source's pair-of-vertices edge model excludes loops.
2. Whether bipartiteness is a property, an explicit partition, or an incidence structure with two
   vertex types, and a checked transport to the source's `paarer Graph` convention.
3. The degree of a vertex counted with edge multiplicity, the definition of maximum degree, and
   how the empty vertex or edge type is handled.
4. Proper edge coloring as a function on edge identities whose restriction to every incident-edge
   fiber is injective, including the color type and the zero-color case.
5. Edge chromatic number as a minimum, an `ENat`, or another representation, and its exact equality
   with the natural maximum degree.
6. Whether the canonical root is the equality, the existence of a proper `Fin Delta` coloring plus
   a separately modeled lower-bound bridge, or a checked equivalence between these forms.
7. Exact ordered binders, hypotheses, conclusion, alternate transports, minimal pinned imports,
   foundation/TCB/computation profiles, and the required removed-hypothesis, changed-domain,
   binder-scope, and boundary mutations.

## Degenerate and boundary cases

Source review and statement mutation must cover the empty vertex type, edgeless graphs, isolated
vertices, `Delta = 0`, one edge, parallel edges with the same endpoints, matchings, stars, paths,
even cycles, disconnected graphs, regular and nonregular graphs, and a supplied bipartition with an
empty side. It must verify that loops are excluded, multiplicity is counted in degree, all incident
parallel edges require distinct colors, and no connectedness or regularity hypothesis is added.

## Excluded substitutions

- A theorem only for `SimpleGraph` is a strict specialization unless a reviewed source-preserving
  transport from multigraphs is supplied.
- Ordinary vertex 2-colorability of a bipartite graph is not edge coloring.
- Vizing's `Delta`/`Delta + 1` theorem for simple graphs and Shannon's multigraph upper bound are
  neighboring results, not this equality.
- Satz B, factorization of regular bipartite graphs into perfect matchings, is a corollary/reduction
  route and cannot replace the nonregular Satz C root.
- A list-edge-coloring theorem, Galvin's theorem, total coloring, or coloring of a special graph
  family is not the received theorem.
- A line-graph coloring without checked equivalence to proper edge coloring and without the
  multigraph boundary does not close the root.
- A stored coloring witness, finite enumeration, theorem name, citation, API probe, or the untrusted
  `已验证` label supplies no source or proof credit.

## Neighbor boundaries

`THM-M-0859` owns Vizing's theorem and `THM-M-0860` owns Shannon's theorem. `THM-M-0812` is
König's bipartite matching/vertex-cover theorem, a distinct theorem despite shared attribution.
`THM-M-0862` is Menger's connectivity theorem. Matching APIs may later support a factorization
proof route, but no neighbor grants proof credit to this target.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned `Mathlib.Combinatorics.Graph.Basic`
provides a source-relevant multigraph representation with edge identity, parallel edges, loops,
links, incidence, and incidence sets, but its current graph modules do not define the needed
multigraph bipartiteness, multiplicity-counted finite degree, proper edge coloring, or chromatic
index. Pinned simple-graph line-graph/coloring APIs also elaborate and expose a possible restricted
encoding. No exact theorem was located in the bounded search. The canonical target, its minimal
imports, expression fingerprint, checked transports, and mutation evidence remain the statement
phase's work.
