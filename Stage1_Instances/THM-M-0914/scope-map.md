# THM-M-0914 scope map

## Preserved catalog claim

The intake preserves exactly the catalog family: for every natural number `n`, any placement of
`n + 1` objects into `n` boxes has a box containing at least two distinct objects. The intended
mathematical content is failure of injectivity when a finite domain has larger cardinality than
the codomain.

This family description is not yet a canonical Lean proposition. The dependent statement phase
must select and independently review one exact encoding and every transport it credits.

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

## Boundary cases to resolve

- `n = 0`, including the empty codomain and absence of a placement function;
- `n = 1`, constant placement of two objects, and the first inhabited case;
- arbitrary finite types with empty domain or codomain;
- exactly `n + 1` objects versus any strictly larger finite domain;
- collision witnesses versus a cardinality-two fiber witness;
- dependence on the chosen `Fintype` structures and transports across finite equivalences.

No boundary case is excluded at intake.

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
The probe establishes declaration availability and the reported axiom surface only. It does not
freeze the catalog's `Fin (n + 1)` target, inspect terminal provenance, or complete an anchor audit.
