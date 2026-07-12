# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0904`, the title `Dinitz猜想`, attribution to Jeff Dinitz, year
1979, and the gloss `列表着色的存在性`. Importance "high" and source status `已证明` are untrusted
catalog metadata, not a mathematical statement or proof receipt.

The title strongly suggests the classical array/list-edge-coloring problem, but the repository does
not state its array, list, color, distinctness, or boundary conventions. Intake therefore preserves
the theorem family without manufacturing a canonical root.

## Candidate array scope, not credited

A familiar candidate formulation is: for a natural number `n`, assign a collection of `n` colors
to every cell of an `n x n` array; then choose one allowed color in each cell so that no chosen color
appears twice in a row or twice in a column. A prospective Lean shape might quantify

```text
n : Nat
Color : Type
L : Fin n -> Fin n -> Finset Color
```

and conclude the existence of `c : Fin n -> Fin n -> Color` satisfying membership in each `L i j`
and injectivity along every fixed row and column. This is a resolution candidate only. It is not the
canonical statement, an elaborated Lean expression, or proof evidence.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted immutable source:

- whether each cell list has cardinality exactly `n` or at least `n`, and the checked direction of
  the finite-list thinning bridge between those forms;
- whether "list" is a finite set, multiset, or duplicate-bearing sequence, and whether duplicate
  entries count toward its size;
- the color carrier and decidable-equality or finiteness assumptions, including whether all cell
  lists must lie in one finite global palette;
- whether `n` ranges over all naturals, only positive naturals, or another finite cardinal, and the
  treatment of `n = 0` and `n = 1`;
- the exact ordered binders and whether row and column conditions use pairwise inequality,
  injectivity, or proper coloring of a graph;
- whether the target is the array problem, list edge-colorability of the simple graph `K_(n,n)`,
  equality of its list chromatic index with `n`, or another formulation;
- the exact source statement, proof boundary, terminology, errata status, and independent review;
  and
- the direction and hypotheses of every transport between array cells, edges of `K_(n,n)`, and a
  line-graph vertex-coloring representation.

## Boundary and degenerate cases

No case is excluded at intake. Source review must decide empty arrays, singleton arrays, empty color
types, insufficient or duplicate-bearing lists, repeated values across different lists, arbitrary
large palettes, and whether row and column distinctness is vacuous in low dimensions. It must also
check that a graph encoding neither loses cells nor admits edges outside the complete bipartite
graph and that conversion between exact-size and lower-bound lists is constructive or declares its
choice principles.

## Neighbor and substitution exclusions

- `THM-M-0905` (Galvin theorem) is a distinct target. Its stronger bipartite-multigraph statement,
  proof, or future receipts do not automatically establish this target.
- Galvin's theorem may later be a bridge to an array statement, but it may not silently replace the
  `K_(n,n)` special case as the canonical claim.
- Ordinary vertex colorability, bipartiteness, existence of a bicoloring, or construction of a line
  graph is not list edge-colorability.
- A statement assuming the desired choice function, proper coloring, matching decomposition, or
  list-coloring result as a field or hypothesis is not the conjecture.
- A Latin square with one common palette is only a special list assignment, not the arbitrary-list
  theorem.
- The catalog's `已证明` label, bibliographic metadata, or an API probe provides no human-source or
  kernel proof credit.

## Downstream boundary

The statement phase must select and independently review one exact proposition before fixing a Lean
module, expression fingerprint, mutation suite, obligation registry, or discovery denominator.
Anchor audit, proof architecture, proof implementation, validation, and release remain separate
open tasks.
