# Scope map

## Frozen human claim

For every finite bipartite graph, the largest cardinality of a set of pairwise
vertex-disjoint edges equals the smallest cardinality of a set of vertices incident to every
edge. Here "maximum" and "minimum" are cardinality extrema, not merely inclusion-maximal or
inclusion-minimal witnesses.

This finite graph-theoretic scope agrees with the repository gloss and the inspected translation
of the 1931 paper. Intake freezes the human claim, but not an exact Lean expression.

## Statement decisions still open

- Resolve whether the source's graph convention is simple or permits parallel edges. The inspected
  translation does not say; a `SimpleGraph` specialization needs source justification or a checked
  transport proving that parallel-edge erasure preserves both extrema.
- If a simple graph is selected, choose `SimpleGraph.IsBipartite` or an explicitly bound
  `SimpleGraph.IsBipartiteWith s t`.
  Mathlib's latter predicate covers graph support, not necessarily isolated vertices, so any
  transport between the forms must be checked.
- Define a maximum matching cardinality compatible with mathlib's representation of a matching as
  `M : G.Subgraph` satisfying `M.IsMatching`. Matching size must count edges, not matched vertices.
- Reconcile that invariant with `SimpleGraph.vertexCoverNum G : ENat`, or select a checked finite
  natural-number encoding for both extrema.
- Freeze the universe, finite-carrier assumptions, ordered binders, decidability and classical
  principle policy, minimal imports, alternate encodings, and expression/environment hashes.
- Mutation-test removed finiteness or bipartiteness, a changed graph domain, altered binder scope,
  and boundary cases before any proof evidence is credited.

## Boundary cases

The translated source starts with a finite bipartite graph and imposes no nonempty condition.
Therefore intake excludes no degenerate graph. Statement work must preserve and test the empty
graph, an edgeless graph with isolated vertices, an empty bipartition side, singleton carriers,
and the zero matching/zero cover equality. Isolated vertices do not affect either extremum.

## Candidate proof architecture

The translated proof supplies a source architecture, not accepted proof obligations:

1. Choose a matching `K` of maximum edge cardinality `M` and orient each matched edge across the
   two bipartition sides.
2. Define alternating `K`-paths from unmatched vertices on the first side. An alternating path to
   an unmatched vertex on the second side would augment `K`, contradicting maximal cardinality.
3. From every matched edge choose its second-side endpoint when it is alternating-reachable and
   its first-side endpoint otherwise. The resulting set has exactly `M` vertices.
4. Prove this set covers an arbitrary edge by four endpoint-membership cases, giving minimum cover
   size at most `M`.
5. Every vertex cover meets each edge of any matching at a distinct endpoint, so every cover has
   at least `M` vertices. Combine the two inequalities.

The obligation phase must refine this architecture and audit the translation before treating it as
a human-source tree.

## Explicit exclusions

- Konig's infinity lemma and the set-theoretic cardinal Konig theorem.
- Konig's bipartite edge-coloring theorem, separately cataloged as `THM-M-0861`.
- Hall's marriage theorem or merely a theorem constructing a matching that saturates one side.
- Infinite-graph cardinal variants without a separately selected source and checked transport.
- A maximal matching in place of a maximum-cardinality matching, or an inclusion-minimal cover in
  place of a minimum-cardinality cover.
- Counting matching vertices without the required factor-of-two relationship to matching edges.
- Proving only the universal easy inequality or only the alternating-path construction.
- Assuming an extremal witness or the desired equality as input data.
- Treating the matrix row/column corollary, a declaration name, an API check, or `已验证` as the
  canonical root or proof evidence.

No canonical Lean expression, statement fingerprint, checked transport, obligation registry,
proof state, or completion claim is frozen at intake.
