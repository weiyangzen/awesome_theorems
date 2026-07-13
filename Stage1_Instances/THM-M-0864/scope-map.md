# Scope map

## Preserved theorem family

The intake preserves the finite undirected 3-connected-graph wheel theorem family identified by the
catalog's phrase `3-连通图的轮分解` ("wheel decomposition of 3-connected graphs"). It does not turn
that phrase into a proposition by silently choosing a standard formulation.

The strongest inspected modern restatement is the minimal form: every minimally 3-connected finite
graph is a wheel, with minimality under both deletion and contraction of every edge. A related
reduction/construction form says that 3-connected graphs can be reduced to wheels by permitted
connectivity-preserving operations, or constructed from wheels by inverse operations. The catalog
does not say whether `轮分解` means the minimal characterization, a contraction sequence, an
edge-splitting construction, or another decomposition statement.

## Decisions required at statement freeze

An accepted exact source statement must decide all of the following:

1. Whether graphs are finite simple graphs, finite multigraphs during contraction, or another model.
2. The definition of 3-vertex-connectivity, including minimum vertex count, deletion of fewer than
   three vertices, separator conventions, and behavior on empty or singleton remainders.
3. Whether the root quantifies over all 3-connected graphs or only minimally 3-connected graphs.
4. For minimality, whether every edge deletion, every edge contraction, or both must destroy
   3-connectivity, and whether contraction is simplified back to a simple graph.
5. The exact wheel graph: cycle/rim size, hub, spoke set, graph-isomorphism representation, and
   whether `K4` is the smallest wheel.
6. If the root is constructive, the permitted edge additions, edge splits, vertex splits,
   contractions, simplifications, sequence orientation, and invariant at every intermediate graph.
7. Whether the conclusion is equality, graph isomorphism, existence of a reduction sequence, an
   inductive generation predicate, or an equivalence between these encodings.
8. Ordered binders, universes, finiteness and decidability typeclasses, hypotheses, conclusion,
   foundation/TCB/computation profiles, and every alternate encoding with a checked transport.

These choices change the proposition or proof boundary. Intake does not choose among them.

## Degenerate and boundary cases

Source review must resolve graphs on zero through four vertices; `K4`; cycles of size zero through
three under mathlib conventions; the minimum admissible rim size; loops and parallel edges created
by contraction; bridges, isolated vertices, complete graphs, and already-wheel graphs; contraction
of a rim or spoke edge; deletion of a rim or spoke edge; empty operation sequences; and whether an
intermediate multigraph is simplified by deleting loops or merging parallel edges.

## Excluded substitutions

- Tutte's perfect-matching theorem is a distinct result despite the shared author and name.
- A theorem about planar/polyhedral graphs only cannot replace a general 3-connected-graph target.
- Whitney's 2-connected ear decomposition, Menger's theorem, the splitter theorem, graph-minor
  decomposition, SPQR trees, and 4-connected decomposition are related but distinct roots.
- Ordinary connectedness, edge connectivity, minimum degree at least three, or the existence of one
  cycle is weaker than 3-vertex-connectivity.
- `SimpleGraph.IsFiveWheelLike` is not the ordinary wheel graph in Tutte's theorem.
- A result for a fixed wheel, fixed vertex count, or only one direction is not the universal theorem.
- A structure or hypothesis storing the desired wheel, reduction sequence, or connectivity result
  supplies no proof.
- The catalog's `已验证` label, a citation, a bounded search, or an API `#check` supplies no H or M
  credit.

## Neighbor boundaries

`THM-M-0862` owns Menger's vertex-connectivity/disjoint-path theorem, `THM-M-0863` Whitney's
2-connected ear decomposition, `THM-M-0865` Kuratowski's planar forbidden-subdivision theorem, and
`THM-M-0866` Wagner's planar-minor theorem. They may later provide definitions or proof dependencies,
but none transfers statement identity or proof status to this target.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks ordinary connectivity, vertex deletion,
cycle graphs, a cycle witness, graph isomorphism, and local vertex/edge operations. The bounded
exact-topic search found no Tutte wheel theorem, 3-vertex-connectivity predicate, ordinary wheel
predicate, or edge-contraction definition. This is scoped intake discovery, not an exhaustive
anchor audit or proof of global absence.
