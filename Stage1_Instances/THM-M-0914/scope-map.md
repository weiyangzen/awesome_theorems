# THM-M-0914 scope map

## Preserved catalog claim

The intake preserves exactly the catalog family: for every natural number `n`, any placement of
`n + 1` objects into `n` boxes has a box containing at least two distinct objects. The intended
mathematical content is failure of injectivity when a finite domain has larger cardinality than
the codomain.

The statement phase selects the literal concrete proposition
`Stage1Instances.THM_M_0914.PigeonholeTarget`: objects are `Fin (n + 1)`, boxes are `Fin n`, and a
placement is a total function. The root concludes with two distinct objects having equal images.
Only the explicit shared-box encoding is credited through a checked iff.

## Proposition-changing decisions

1. **Objects and boxes:** choose the concrete types `Fin (n + 1)` and `Fin n`, or arbitrary finite
   types with a strict cardinality hypothesis. The latter is a broader theorem unless a checked
   specialization and source relationship are supplied.
2. **Placement:** model every object as occupying exactly one box, normally by a total function.
   Partial placements, relations, multisets, and capacity constraints are different statements.
3. **Conclusion:** choose distinct `x y` with `f x = f y`, noninjectivity, or a box whose fiber has
   cardinality at least two. These require checked equivalence or implication witnesses before
   they share credit.
4. **Natural-number syntax:** fix whether the object count is written `n + 1`, `Nat.succ n`, or
   only as `n < m`; do not broaden the root without a checked map.
5. **Zero boxes:** for `n = 0`, no total function `Fin 1 -> Fin 0` exists. A universally quantified
   function statement is vacuously true because the function binder has no inhabitants, whereas
   a fiber-witness conclusion cannot exhibit a box. The statement must preserve this boundary.
6. **Finite structures and universes:** fix the type universes, `Fintype` instances, equality and
   decidability requirements, and any choice or classical policy.

## Frozen boundary cases

- `n = 0` is included. The function binder is empty because there is no `Fin 1 -> Fin 0`;
  `no_placement_into_zero_boxes` checks this representation.
- `n = 1` is included. `one_box_boundary` checks the first inhabited two-object collision.
- Exactly `n + 1` objects are in the root; arbitrary larger domains are downstream variants.
- An explicit common-box witness is checked equivalent; a fiber-cardinality predicate is not
  credited.
- No `Fintype` structures or finite-equivalence transports occur in the concrete root.

No natural-number case is excluded.

## Explicit exclusions

- the generalized `m > n` theorem used as the root without a checked specialization;
- generalized fiber lower bounds, weighted pigeonhole principles, or average-fiber results;
- infinite pigeonhole and cardinal/cofinality variants;
- probabilistic, measure-theoretic, geometric, or topological pigeonhole analogues;
- Haken's resolution proof-length lower bound (`THM-M-0691`);
- Hall's marriage theorem, matching theorems, inclusion-exclusion, or Ramsey theory;
- assuming injectivity fails, assuming a collision, or storing the desired box/witness in a
  hypothesis or structure;
- a theorem name, API probe, catalog status, example, or finite computation used as proof credit.

## Neighbor boundaries

- `THM-M-0913` is inclusion-exclusion, a distinct counting identity.
- `THM-M-0915` concerns generating-function methods, not finite-function collisions.
- `THM-M-0691` concerns resolution-proof complexity for a propositional pigeonhole formula, not
  the ordinary combinatorial theorem.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the exact-family
candidate is:

```text
Fintype.exists_ne_map_eq_of_card_lt
  (f : alpha -> beta)
  (h : Fintype.card beta < Fintype.card alpha) :
  exists x y, x != y and f x = f y
```

The source module also provides the embedding formulation and adjacent finite/infinite variants.
The intake probe establishes declaration availability and the reported axiom surface only. The
statement module separately freezes the catalog's `Fin (n + 1)` target without importing this
candidate. Terminal provenance and the complete anchor audit remain downstream.
