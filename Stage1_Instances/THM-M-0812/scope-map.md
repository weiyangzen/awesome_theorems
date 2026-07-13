# Scope map

## Frozen human claim

For every finite bipartite graph, the largest cardinality of a set of pairwise
vertex-disjoint edges equals the smallest cardinality of a set of vertices incident to every
edge. Here "maximum" and "minimum" are cardinality extrema, not merely inclusion-maximal or
inclusion-minimal witnesses.

This finite graph-theoretic scope agrees with the repository gloss and the inspected translation
of the 1931 paper. Intake froze the human claim; the statement phase subsequently froze its exact
Lean expression.

## Statement decisions

- The canonical target uses finite types `L`, `R`, and `E`, with endpoint maps `E -> L` and
  `E -> R`. This makes the bipartition explicit and preserves parallel-edge identity.
- `IsEdgeMatching` requires both endpoint maps to be injective on a selected edge set, so matching
  size is the number of edges rather than the number of incident vertices.
- `HasMatchingNumber` and `HasVertexCoverNumber` separately require an attained witness and a
  universal bound at one shared natural number.
- `konigMatchingCoverTarget_iff_simpleRelationKonigTarget` kernel-checks that retaining one edge
  representative per occupied endpoint pair preserves both extrema. Thus the source's silent
  simple-versus-parallel convention does not change the selected claim.
- `konigMatchingCoverTarget_iff_expanded` checks the binder-complete expansion. The statement
  packet freezes universes, ordered binders, two minimal imports, environment/expression hashes,
  four mutation classes, and boundary proofs.
- One-sorted `SimpleGraph.IsBipartite`, explicit `IsBipartiteWith`, mathlib `Graph`, and matrix
  transports remain uncredited alternate interfaces for later audit; they do not make the exact
  local incidence target ambiguous.

## Boundary cases

The translated source starts with a finite bipartite graph and imposes no nonempty condition.
Therefore the target excludes no degenerate graph. `edgelessBoundary` verifies the zero
matching/zero cover equality with arbitrary finite sides, including empty sides and isolated
vertices, while `singleEdgeBoundary` verifies both extrema are one. Singleton carriers and
parallel edges remain admitted.

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

The canonical Lean expression, statement fingerprint, expanded transport, and simple-relation
transport are now frozen by statement artifacts. No obligation registry, proof state, accepted
execution state, audit completion, or theorem-completion claim is frozen.
