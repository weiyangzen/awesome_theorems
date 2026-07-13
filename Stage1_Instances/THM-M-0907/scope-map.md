# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0907`, title `Alon-Tarsi定理`, attribution Noga Alon/Michael
Tarsi, year 1992, and the gloss `列表着色的组合Nullstellensatz方法`. It supplies no bibliography,
formula, graph model, definitions, binders, hypotheses, conclusion, proof locator, correction
history, or formal artifact. Importance `高` and status `已验证` are inventory metadata only.

The gloss identifies an algebraic list-coloring theorem family but is not one stable proposition.
The word `方法` (method) especially leaves open whether the target owns the main orientation
criterion, its graph-polynomial coefficient lemma, a generic polynomial lemma, a choosability
corollary, or a methodological package.

## Primary candidate, not canonical

The strongest candidate is Theorem 1.1 of Alon and Tarsi, *Colorings and orientations of graphs*.
In source notation it considers a digraph `D = (V,E)`. For every vertex `v`, an allowed set `S(v)`
contains exactly `d_D^+(v) + 1` distinct integers. If `EE(D) != EO(D)`, where these count even and
odd Eulerian spanning subdigraphs and the empty subdigraph is even, then there is a legal vertex
coloring `c : V -> Z` with `c(v) in S(v)` for every vertex.

This statement is a resolution candidate only. It is not the canonical mathematical statement, an
elaborated Lean expression, or accepted proof evidence.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted, independently reviewed
source:

- whether the root is Theorem 1.1, Corollary 1.2, Corollary 2.3, Proposition 2.7, a theorem from
  Section 3, or an explicitly structured package;
- whether `D` is a finite loopless orientation of a finite simple undirected graph, and whether
  antiparallel arcs, loops, or parallel edges are permitted;
- the underlying undirected adjacency used by `legal vertex-coloring`, including the treatment of
  a pair joined in one direction, both directions, or by a loop;
- whether an Eulerian subgraph is a spanning edge-subset subdigraph, how indegree and outdegree are
  counted, whether disconnected subgraphs are allowed, and whether the empty subgraph is included;
- whether `EE` and `EO` are natural-number cardinalities, an integer signed difference, or a graph-
  polynomial coefficient, and every finiteness/decidability premise required to define them;
- whether allowed colors are finite sets of distinct integers of cardinality exactly
  `outdegree(v) + 1`, sets of at least that size with a checked thinning bridge, or lists/multisets
  with explicit duplicate semantics;
- the exact proper-coloring condition, all ordered binders, universes, coercions, typeclasses, and
  classical-choice requirements;
- whether the proof is reconstructed through the paper's integer interpolation Lemma 2.1 or the
  pinned 1999 Combinatorial Nullstellensatz, and the checked implication relating those routes; and
- the exact source edition, theorem/page mapping, proof boundary, corrections or errata, and
  independent reviewer approval.

## Boundary cases

No case is excluded at intake. Source and statement review must decide empty vertex and edge sets,
one vertex, edgeless digraphs, isolated vertices, self-loops, antiparallel arcs, disconnected graphs,
empty and singleton Eulerian subgraphs, zero outdegree, empty color carriers, exact versus oversized
lists, and whether a loop makes legal coloring impossible. It must also show that the chosen Lean
digraph representation neither invents multiplicity nor loses the source orientation.

## Neighbor and substitution exclusions

- `THM-M-0906` owns general list-coloring theory; its definitions or future receipts do not prove
  the Alon-Tarsi criterion.
- `THM-M-0904` (Dinitz conjecture) and `THM-M-0905` (Galvin theorem) own distinct list-edge-
  coloring claims. The conditional Dinitz discussion in the 1992 paper cannot be substituted here.
- `THM-M-0908` owns a planar-graph list-chromatic result; a planar special case is not this target.
- Pinned `Mathlib.Combinatorics.Nullstellensatz` formalizes Alon's later generic polynomial theorem.
  It is an ingredient candidate, not the graph orientation/parity/list-coloring result.
- Ordinary `SimpleGraph.Colorable`, a bicoloring, an acyclic-orientation special case, the
  no-odd-directed-cycle corollary, or one explicit graph instance is not the full candidate root.
- A structure or hypothesis storing the desired coloring, Eulerian-count inequality, nonzero
  coefficient, or conclusion is not a proof of the theorem.
- The catalog label, DOI, source PDF, theorem name, API probe, or passing unrelated build grants no
  human-source or kernel proof credit.

## Downstream boundary

The statement phase must admit and independently review one exact root before it fixes a Lean
module, expression/environment fingerprint, transports, or mutations. Anchor audit, obligation
registry, proof architecture, implementation, validation, and release remain separate open tasks.
