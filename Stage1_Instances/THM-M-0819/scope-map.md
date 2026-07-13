# Scope map

## Preserved theorem family

The catalog fixes the eponym, Robert Dilworth, the year 1950, and chain decomposition of a poset.
The intended root must remain the chain-partition versus antichain-width theorem. Intake does not
silently choose among these materially different formulations:

1. **Primary finite-width form.** For an arbitrary poset and finite `k`, if no independent subset
   has `k + 1` elements and some independent subset has `k` elements, the carrier is the disjoint
   union of `k` chains.
2. **Modern finite-poset equality.** For a finite poset, the minimum cardinality of a chain
   partition equals the maximum cardinality of an antichain.
3. **Cover form.** The minimum number of chains whose union covers the carrier equals its width,
   without requiring those chains to be disjoint as input. An additional theorem is needed to
   relate an optimal overlapping cover to a partition.
4. **Cardinal or infinite extensions.** Statements for infinite width, arbitrary cardinal
   decompositions, or choice-sensitive variants are outside the usual finite equality and require
   their own foundation and source review.

## Decisions required at statement freeze

1. Select the primary Theorem 1.1 form or the standard finite-poset equality and independently
   approve the transport between them in the credited direction.
2. Fix the carrier representation: a finite type with `[PartialOrder alpha]`, a finite subset of an
   ambient poset, or an arbitrary poset with a natural-number width bound.
3. Define a chain using pairwise comparability under `(<=)` and an antichain using distinct elements
   pairwise unrelated by `(<=)`. Decide whether a preorder is rejected or quotiented.
4. Decide whether a chain family is a disjoint partition, a unique-membership family, or merely a
   cover, and whether duplicate or empty chain members are allowed.
5. Fix the optimization codomain (`Nat`, `ENat`, or `Cardinal`) and prove that the relevant minimum
   and maximum are attained rather than only taking an infimum or supremum.
6. Resolve the empty poset, singleton poset, total order, discrete order, `k = 0`, and `k = 1`,
   including whether the empty partition is the unique zero-chain witness.
7. Freeze ordered binders, universes, typeclasses, exact imports, logical principles, and every
   alternate encoding with a checked source-approved transport.
8. Reconcile the external candidate with current mathlib's `Set.chainHeight` refactor, then rerun
   exact-type, axiom, placeholder, provenance, and statement-mutation checks.

## Explicit exclusions

- Mirsky's dual theorem, which equates maximum chain size with a minimum antichain partition.
- The infinite/cardinal Dilworth theorem substituted for the finite equality, or conversely,
  without an approved checked relationship.
- Hall's marriage theorem, Konig's theorem, maximum matching/minimum vertex cover, graph coloring,
  or comparability-graph perfection used as a substitute root rather than an explicit reduction.
- Only the easy lower bound that every chain cover has at least as many members as any antichain.
- An existence theorem whose width or maximum antichain is supplied as an assumed witness but whose
  minimum-chain equality is not proved.
- A chain cover with overlaps presented as a disjoint decomposition without a checked refinement.
- A finite result restricted to a convenient special poset class, or a preorder result that loses
  antisymmetry without an explicit quotient transport.
- The catalog's `已验证` label, a theorem name, `#check`, source URL, or failed external build treated
  as source acceptance, kernel closure, or theorem completion.

`THM-M-0820` owns Mirsky's theorem and `THM-M-0821` owns Sperner's theorem. Their future artifacts
may become explicit dependencies only after statement and obligation freezes; proximity transfers
no status or proof credit.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
