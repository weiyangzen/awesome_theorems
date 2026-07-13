# Scope map

## Repository boundary

- Target: `THM-M-0841`, "Erdos-Stone theorem", graph-theory category.
- Attribution/year: Paul Erdos and A. H. Stone, 1946.
- Literal catalog gloss: "a fundamental theorem of extremal graph theory".
- Lifecycle: `planned` from the uniform `L0 / rework_required` baseline.
- The catalog's `已验证` label is untrusted metadata and grants no source or machine credit.

## Selected canonical theorem

The statement phase selects the only theorem named in the attributed primary paper:

1. **Canonical original-paper containment form.** Given `0 < epsilon < 1` and an integer `r >= 2`, every
   sufficiently large graph which has fewer than
   `(1 / (2 * (r - 1)) - epsilon) * n^2` edges contains `r` disjoint vertex groups, each of an
   explicit iterated-logarithmic size, with no cross-group edges. Its dense-complement restatement
   has complete cross-group edges, with eventual slack needed when translating the edge threshold.
2. **Uncredited modern extremal-density form.** For a fixed finite simple graph `H` of chromatic number at
   least two, the maximum number of edges in an `H`-free `n`-vertex graph is asymptotic to
   `(1 - 1 / (chi(H) - 1)) * n^2 / 2`; equivalently its Turan density is that coefficient.

The exact correspondence between the selected 1946 statement and the modern fixed-forbidden-graph
formula is proof-bearing mathematics, not a naming convention. It remains downstream work and the
modern form receives no statement identity or proof credit.

## Frozen statement decisions

- Root: the sparse page-1087 finite threshold/containment theorem, not the modern density theorem.
- Edge normalization: the source's `n^2` expression and strict "fewer than" comparison.
- Quantifiers: `epsilon`, then `r`, their three premises, then existential `n0`, universal `n > n0`,
  and universal labeled graph with decidable adjacency.
- Groups: an existential positive natural `k` at least `sqrt(l_(r-1)(n))`, encoded by containment of
  `completeEquipartiteGraph r k` in the complement.
- Iterated logarithm: `Real.log^[j] x`, so iteration zero is identity and iteration one is `log`.
- Boundaries: `epsilon = 0`, `epsilon >= 1`, `r = 0`, `r = 1`, and `n <= n0` are excluded exactly
  by the antecedents. No fixed-forbidden-graph or chromatic-number data enter the canonical root.

## Pinned Lean boundary

Pinned mathlib models the selected target with exactly two direct imports:

- `Mathlib.Analysis.SpecialFunctions.Log.Basic` supplies `Real`, natural logarithm, square root,
  real casts, and the imported iteration vocabulary;
- `Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite` supplies finite simple graphs, edge
  finsets, complements, non-induced containment, and equal-part complete graphs.

Deleting either direct import makes the exact module fail. The pinned tree has no
`ErdosStoneSimonovits.lean` module or proof of the target. A later commit object visible in the
package repository is not an input in the pinned dependency tree and receives no proof credit.

## Explicit exclusions

- Turan's theorem alone, the clique-only special case, or general existence of Turan density as a
  substitute for Erdos-Stone.
- Simonovits stability (`THM-M-0842`), the removal lemma, regularity lemma, supersaturation, or a
  minimum-degree strengthening as a silently substituted root.
- A theorem assuming the desired complete-equipartite copy, asymptotic formula, or density equality.
- Any unpinned branch/commit object, theorem name, documentation index entry, or catalog status as
  kernel evidence.
- Hypergraph, directed, weighted, infinite-graph, graphon, or probabilistic variants.

## Current cut set

Dependency-ordered master acceptance, independent source review, checked transport to other common
forms, formal-candidate/provenance audit, obligation and discovery freezes, proof and composition,
readable reconstruction, trust closure, hermetic replay, independent release validation, and master
release acceptance remain open.
