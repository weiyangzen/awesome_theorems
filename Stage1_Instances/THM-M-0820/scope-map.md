# Scope map

## Preserved theorem family

The intake preserves the finite-poset equality between two optimization quantities:

- the least number of antichains in a cover of the entire carrier; and
- the greatest number of elements in a chain.

An inspected Coq source uses a possibly overlapping antichain cover. The common partition form is
expected to be equivalent by disjointizing a cover without adding parts, but that transport is not
credited until checked. This is a theorem-family description, not the canonical Lean target.

## Proposition-changing decisions

The dependent statement phase must fix all of the following from one immutable source passage:

- whether the carrier is a finite type, a finite subset of a larger poset, or a finite poset
  structure, and whether nonemptiness is assumed;
- whether a chain uses `<=` comparability or strict order, and whether height counts elements or
  strict steps (these differ by one for nonempty chains);
- whether the canonical form is the source-matched possibly overlapping cover, an exact
  pairwise-disjoint partition, a
  `Finpartition`, a coloring by height levels, or another source-equivalent encoding;
- whether the conclusion is an equality of minima/maxima, a least-cardinality witness, or the two
  inequalities plus a constructed partition;
- all decidability and finiteness instances, universe parameters, ordered binders, and classical
  choice commitments; and
- the empty-poset, singleton, total-order, discrete-order, and repeated-level boundaries.

## Included boundaries

- A singleton poset has maximum chain cardinality one and needs one nonempty antichain part.
- An `n`-element total order needs `n` singleton antichains.
- An `n`-element discrete order is itself one antichain when `n > 0`.
- Comparable elements cannot lie in the same antichain, which supplies the lower bound from any
  maximum chain.
- A level/rank construction may supply the upper bound only after it is proved to cover the entire
  carrier, have disjoint fibers, and make every fiber an antichain.
- If the empty poset is admitted, its minimum partition size and maximum chain cardinality must use
  matching zero conventions rather than silently importing a nonempty theorem.

## Explicit exclusions

- Dilworth's theorem, which exchanges the roles of chains and antichains, is not a substitute.
- Sperner's theorem for the Boolean lattice is only a specialized width result.
- Existence of some antichain cover without minimality, or only the lower-bound inequality, does
  not close the equality.
- A partition does not silently replace the inspected source's possibly overlapping cover unless a
  checked disjointization preserves the optimum and antichain property.
- `Set.chainHeight`, `Order.height`, `IsAntichain`, or `Finpartition` alone is vocabulary, not
  Mirsky's theorem.
- Infinite-poset, ordinal-height, well-founded-rank, graph-coloring, or dual-Dilworth statements
  require checked transports and cannot be silently substituted.

## Downstream route

`STATEMENT` must select one source-faithful finite formulation, elaborate it under minimal pinned
imports, serialize the expression and environment fingerprints, check credited alternate
encodings, and mutation-test finiteness, height convention, binder scope, and boundary cases.
Candidate provenance, proof architecture, proof integration, trust closure, readable
reconstruction, and release remain later nodes.
