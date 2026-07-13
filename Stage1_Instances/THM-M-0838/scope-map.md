# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0838`, the title `Gonthier的形式化证明`, attribution Georges
Gonthier, year 2008, and the gloss `四色定理的Coq形式化`. It categorizes the item as a theorem or
proposition but supplies no formula, definition chain, theorem locator, toolchain, dependency pin,
or proof-body receipt. Intake preserves this provenance-specific Four Color formalization identity
without inheriting the untrusted `已验证` status.

The located Coq root is a strong scope anchor, not yet the selected Lean proposition. In the
historical source it has the shape:

```text
forall m : map R, simple_map m -> map_colorable 4 m
```

Here `R` is an abstract real model; a map relates real-plane points into regions; `simple_map`
requires a proper map with open connected regions; and `map_colorable 4` existentially supplies a
proper coloring map with at most four regions. The maintained source uses equivalent renamed
interfaces `Real.model`, `finite_simple_map`, `simple_map`, and `colorable_with 4`.

## Root decision required

The statement phase must select and independently approve exactly one target boundary:

1. The mathematical Coq root proposition, transported faithfully into Lean.
2. An artifact claim that a pinned Coq/Rocq development kernel-checks the exact `four_color`
   declaration under a recorded toolchain, dependencies, axioms, and trust policy.
3. An explicit conjunction connecting the source proposition, the pinned upstream declaration,
   and a checked Lean encoding or transport.

These are not interchangeable. A generic planar-simple-graph theorem erases the source map model
and the item's provenance distinction. An upstream build claim is not itself a Lean proof. A
mathematical theorem does not by itself establish the history or integrity of a particular artifact.

## Proposition-changing decisions

An approved statement must freeze:

1. The real model, plane-point and region constructions, and any classical-real or excluded-middle
   assumptions inherited from the source.
2. The definition of map, properness, region equality, openness, connectedness, cover, border,
   corner, adjacency, coloring, and number of colors.
3. Finite versus arbitrary simple maps and the compactness bridge from `four_color_finite` to
   `four_color`.
4. The relationship between face/map coloring, hypermap coloring, and vertex coloring of a planar
   simple graph, including duality and representation hypotheses in every direction credited.
5. Connectedness, bridges, loops, parallel edges, isolated regions, infinite maps, and empty or
   degenerate maps.
6. Whether four means a palette of exactly four names or colorability with at most four colors.
7. Ordered binders, universes, coercions, typeclasses, hypotheses, conclusion, foundation profile,
   toolchain boundary, and every checked alternate encoding.

## Candidate scopes not credited

- The exact historical Coq declaration `four_color` over `real_model`, `map`, `simple_map`, and
  `map_colorable 4`.
- The maintained declaration `four_color` over `Real.model`, `map`, `simple_map`, and
  `colorable_with 4`.
- The finite-map declaration `four_color_finite` plus the compactness extension.
- The intermediate combinatorial declaration `four_color_hypermap` for planar bridgeless
  hypermaps.
- A Lean theorem saying every source-faithful encoding of a simple map is colorable with four
  colors.
- A generic Lean theorem saying every graph satisfying a separately defined planarity predicate is
  `SimpleGraph.Colorable 4`, but only with checked transports to and from the source model.
- A provenance theorem about an immutable upstream Coq declaration and its kernel evidence.

## Excluded substitutions

- `THM-M-0833` generic Four Color Theorem, `THM-M-0836` Appel-Haken computer proof, or
  `THM-M-0837` Robertson-Sanders-Seymour-Thomas proof used as inherited status.
- The five-color theorem, a three-color special class, bipartite or outerplanar cases, finite
  enumerations, small graphs, or a fixed map.
- `four_color_hypermap` presented as the final real-plane map theorem without discretization and
  compactness composition.
- Face/map coloring presented as vertex coloring of arbitrary planar simple graphs, or conversely,
  without checked duality and representation transports.
- A predicate, structure, or hypothesis that stores planarity, a four-coloring, or the desired
  source declaration as input.
- A theorem name, article prose, repository README, CI badge, `#check`, API schema, computation log,
  or the catalog's `已验证` label used as source or proof credit.
- Coq/Rocq kernel closure reported as Lean kernel closure, or a URL/commit used as repo-local M0.

## Neighbor ownership

`THM-M-0833` owns the generic mathematical theorem. `THM-M-0836` owns the Appel-Haken
computer-assisted proof, and `THM-M-0837` the later Robertson-Sanders-Seymour-Thomas proof.
This target owns only the catalog's Gonthier/Coq formalization identity. Any shared mathematical
root, source node, or machine body must be represented later through explicit typed provenance and
composition edges; proximity supplies no duplicated credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib's
`Mathlib.Combinatorics.SimpleGraph.Coloring` provides `SimpleGraph.Coloring`, `Colorable`, and the
chromatic-number equivalence, but no source-faithful real-plane map model or accepted planarity
bridge. The module's own TODO lists planar graphs. The discovery probe elaborates a parameterized
schema only. Exact imports, expression and environment fingerprints, transports, mutations, and
formal-candidate provenance belong to later phases.
