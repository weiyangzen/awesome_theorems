# Scope map

## Preserved source scope

The candidate root is the theorem printed on page 194 of Brooks's 1941 note. A source-faithful
encoding must preserve all of these components:

- `n` is a natural-number color/degree bound satisfying `2 < n`.
- The vertex carrier may be infinite and the graph need not be planar.
- At most `n` lines meet each node, encoded prospectively as pointwise finite degree at most `n`.
- No line has both ends at the same node; Lean `SimpleGraph` supplies looplessness.
- No connected component is an `n`-simplex, which Brooks immediately defines as `n + 1` nodes with
  every pair joined.
- The conclusion is a proper node coloring using `n` colors, prospectively `G.Colorable n`.

The all-components formulation is material. The printed proof then reduces to a connected network,
but connectedness is not a root hypothesis. The source also says that the hypotheses make a
connected network finite or enumerable; countability is a derived proof fact, not an extra root
assumption.

## Decisions required at statement freeze

1. Preserve and hash a lawful immutable copy of all four pages, record the exact theorem and proof
   boundary, inspect corrections or errata, and obtain independent source review.
2. Confirm that the catalog's `Rowland Brooks` and the paper's `R. L. Brooks` identify the same
   target and that the catalog gloss selects the printed theorem rather than only a modern corollary.
3. Determine whether Brooks's use of "network (or linear graph)" permits parallel lines. If it
   does, either justify the simple-graph reduction without changing degrees or select a faithful
   multigraph encoding. Lean `SimpleGraph` cannot represent parallel edges.
4. Freeze the exact universe, binder order, instance arguments, pointwise degree encoding, strict
   inequality `2 < n`, component graph, `n`-simplex predicate, and colorability conclusion.
5. Decide whether `Nonempty (H ≃g completeGraph (Fin (n + 1)))` is the canonical `n`-simplex
   encoding or a checked alternate to a direct cardinality/completeness predicate.
6. Mutation-test removal of the degree/component hypotheses, a finite-carrier domain change,
   connected-versus-all-components binder scope, and the boundary `n = 2`.

## Explicit exclusions

- The common finite connected statement `chi(G) <= Delta(G)` unless `G` is complete or an odd
  cycle, unless a reviewed and checked transport relates it to the selected 1941 root.
- A finite-only theorem: page 194 explicitly permits infinite networks.
- A connected-only theorem: the printed root quantifies over all components.
- A theorem with `n = 2`: odd cycles show why Brooks states `n > 2`.
- Replacing "degree at most `n`" with regularity, minimum degree, average degree, degeneracy, or a
  bound by the cardinality of the vertex type.
- Excluding only a complete subgraph or clique; the source excludes a complete connected component.
- Edge coloring, list coloring, Brooks-type later refinements, or Robert Brooks's spectral theorem.
- An assumed coloring field, an axiom, a placeholder, the untrusted catalog label, or an adjacent
  mathlib coloring theorem used as proof evidence.

## Formal boundary

Pinned mathlib provides `SimpleGraph.Colorable`, `LocallyFinite`, `degree`, connected-component
graphs, graph isomorphisms, and complete graphs. The checked intake envelope uses precisely those
interfaces and allows an arbitrary vertex type. A bounded exact-topic search found no Brooks
declaration or theorem relating the maximum/pointwise degree bound to colorability. This is intake
feasibility evidence only, not the downstream exhaustive anchor audit or proof of global absence.
