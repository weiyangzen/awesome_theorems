# Scope map

## Included claim

- An arbitrary carrier, with no finiteness, countability, or pre-existing order assumption.
- Existence of a strict relation which is both a strict linear order and well-founded.
- The equivalent structure surface: a `LinearOrder` whose `<` relation is well-founded.
- Empty, singleton, finite, and infinite carriers.
- Explicit accounting for the theorem's classical-choice foundation.

## Decisions deferred to statement freeze

- The exact universe binder and whether the canonical surface is `Type u` only or includes a
  separately justified set-model transport.
- Whether the canonical Lean root uses `Nonempty { r // IsWellOrder alpha r }` or
  `exists_wellOrder`'s existential `LinearOrder` surface.
- Checked transports among `IsWellOrder`, `LinearOrder` plus `WellFoundedLT`, and the selected
  `WellOrderingRel` implementation.
- Mutation tests replacing well-order by linear order alone, well-founded relation alone, a fixed
  familiar order, and a restricted carrier domain.

## Explicit exclusions

- The fact that a particular already ordered type such as `Nat` is well-ordered.
- Well-founded partial orders and well-quasi-orders, which do not assert a well-order.
- A relation or order supplied as an extra hypothesis followed by a tautological existential.
- The axiom of choice, Zorn's lemma, or a maximal-chain principle as the root without a checked
  equivalence transport.
- Treating `WellOrderingRel` as constructive or hiding its use of `Classical.choice`.
- Treating the repository label `已验证` as source or machine evidence.
