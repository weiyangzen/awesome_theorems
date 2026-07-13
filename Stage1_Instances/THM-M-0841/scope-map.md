# Scope map

## Repository boundary

- Target: `THM-M-0841`, "Erdos-Stone theorem", graph-theory category.
- Attribution/year: Paul Erdos and A. H. Stone, 1946.
- Literal catalog gloss: "a fundamental theorem of extremal graph theory".
- Lifecycle: `planned` from the uniform `L0 / rework_required` baseline.
- The catalog's `已验证` label is untrusted metadata and grants no source or machine credit.

## Included theorem family

The intended family is an asymptotic extremal result for finite simple graphs. It relates high edge
density, containment of complete equipartite subgraphs, and the chromatic number of a fixed
forbidden graph. Intake retains both of these closely related forms without declaring them equal:

1. **Original-paper containment form.** Given `epsilon > 0` and an integer `r >= 2`, every
   sufficiently large graph which has fewer than
   `(1 / (2 * (r - 1)) - epsilon) * n^2` edges contains `r` disjoint vertex groups, each of an
   explicit iterated-logarithmic size, with no cross-group edges. Its dense-complement restatement
   has complete cross-group edges, with eventual slack needed when translating the edge threshold.
2. **Modern extremal-density form.** For a fixed finite simple graph `H` of chromatic number at
   least two, the maximum number of edges in an `H`-free `n`-vertex graph is asymptotic to
   `(1 - 1 / (chi(H) - 1)) * n^2 / 2`; equivalently its Turan density is that coefficient.

The exact correspondence between the 1946 complete-equipartite statement and the modern
fixed-forbidden-graph formula is proof-bearing mathematics, not a naming convention. It remains a
statement/source task.

## Decisions deferred to statement freeze

- Whether the root is the paper's finite threshold/containment theorem, the modern chromatic-number
  extremal-number asymptotic, or a source-reviewed checked equivalence package containing both.
- Whether density is normalized by `n^2`, `n.choose 2`, or a real-valued interpolation, and how the
  two normalizations are transported.
- The exact meaning and domain of chromatic number, especially `chi(H) = 0`, `1`, `2`, or infinity.
- Whether the forbidden graph is required to be finite, nonempty, to contain an edge, or merely to
  have finite chromatic number at least two.
- Strict versus non-strict edge inequalities, natural-to-real coercions, threshold quantifier
  order, and the exact `epsilon` range.
- The original paper's complement convention, `r` versus `r + 1` indexing, iterated logarithm,
  floor/ceiling, and lower-bound convention for the equal part size.
- Empty vertex types, `r = 0` or `1`, zero part size, empty and complete forbidden graphs, and
  graphs below the eventual threshold.

## Pinned Lean boundary

Pinned mathlib models all major nouns needed to state candidate variants:

- `SimpleGraph.extremalNumber` and `SimpleGraph.turanDensity`;
- `SimpleGraph.tendsto_turanDensity` and general containment above Turan density;
- `SimpleGraph.completeEquipartiteGraph` and `CompleteEquipartiteSubgraph`;
- complete multipartite graph colorings and chromatic number.

The pinned tree has no `ErdosStoneSimonovits.lean` module and no theorem computing `turanDensity H`
from `H.chromaticNumber`. A later commit object visible in the package repository is not an input in
the pinned dependency tree and receives no proof credit.

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

Exact variant selection and independent source review, canonical Lean elaboration and mutations,
formal-candidate/provenance audit, obligation and discovery freezes, proof and composition, readable
reconstruction, trust closure, hermetic replay, independent release validation, and master
acceptance all remain open.
