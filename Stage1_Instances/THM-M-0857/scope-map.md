# Scope map

## Included theorem family

- A graph in which every vertex has degree three.
- A hypothesis excluding bridge edges.
- Existence of a spanning degree-one factor, expressed in modern language as a perfect matching.
- The finite graph-theory result conventionally called Petersen's theorem.

This is a family boundary, not a frozen proposition. A candidate Lean-facing simple-graph form is:

```text
for finite V and G : SimpleGraph V,
G.IsRegularOfDegree 3 ->
(forall e, not G.IsBridge e) ->
exists M : G.Subgraph, M.IsPerfectMatching
```

It is recorded only to expose the statement choices. It has not been selected, elaborated,
fingerprinted, transported from the primary source, mutation-tested, or credited.

## Choices required at statement freeze

1. **Graph model:** Petersen explicitly permits parallel edges, whereas mathlib `SimpleGraph`
   excludes loops and parallel edges. Select a multigraph theorem or approve a source-faithful
   simple-graph specialization with a checked domain boundary.
2. **Finiteness:** the catalog omits it. The historical paper operates on finite regular graphs;
   an infinite regular-graph statement is not silently included.
3. **Connectedness:** Petersen normally treats connected graphs. The modern simple-graph claim can
   be stated componentwise without connectedness, but that extension needs an explicit source or
   checked transport.
4. **Cubic:** decide whether degree three counts incident edge multiplicity or distinct neighbors.
   `SimpleGraph.IsRegularOfDegree 3` uses finite neighbor-set cardinality.
5. **Bridgeless:** choose `forall e, not G.IsBridge e`, quantification only over `G.edgeSet`, or a
   reviewed edge-connectivity formulation. `IsEdgeConnected 2` also imposes preconnectedness and
   is not a definitionally interchangeable slogan.
6. **Perfect matching:** choose a spanning matching subgraph, a degree-one factor, or a set of
   disjoint edges, and provide checked transports for every credited alternate encoding.

## Boundary cases to resolve

- empty and singleton vertex types;
- disconnected unions of cubic components;
- loops and parallel edges in the historical model;
- finite versus locally finite or arbitrary infinite graphs;
- bridge quantification over all `Sym2 V` values versus present edges;
- decidable equality and adjacency instances used only for computation;
- equivalence between a perfect matching and the complement of a two-factor.

## Explicit exclusions

- the Petersen graph as an example rather than the universal theorem;
- Tutte's theorem alone without the cubic-bridgeless-to-Tutte-condition argument;
- a simple-graph theorem silently substituted for an intended multigraph theorem;
- stronger variants allowing a bounded number of bridges unless separately transported;
- a two-factor conclusion without a checked equivalence to a perfect matching;
- a matching witness, Tutte condition, or desired factor assumed as input;
- a fixed-cardinality, connected-only, bipartite-only, planar-only, or numerical special case;
- the repository's untrusted verified label or the API probe as proof credit.

No degenerate case is excluded and no canonical Lean target is frozen at intake.
