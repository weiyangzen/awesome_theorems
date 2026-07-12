# Scope map

## Included claim

- An arbitrary indexed family `A i`.
- A nonemptiness witness for every fiber.
- Existence of one simultaneous selector, represented as a dependent function.
- Empty index types, for which the selector exists vacuously.
- Explicit reporting that the Lean closure rests on foundational choice.

## Decisions deferred to statement freeze

- Exact `Type`/`Sort` universe levels and binder ordering.
- Whether the canonical surface uses `Nonempty (∀ i, A i)` or an existential selector for sets.
- Checked transports to set membership, right inverses of surjections, and nonempty products.
- Mutation tests deleting fiber nonemptiness, replacing all families by countable families, and
  changing dependent fibers to a constant family.

## Explicit exclusions

- Countable choice or dependent choice as a broadened or weakened substitute.
- Unique choice, which has different constructive strength.
- The well-ordering theorem or Zorn's lemma without a checked equivalence transport.
- A selector supplied as an extra hypothesis followed by a tautological projection.
- Treating `Classical.choice` as a derived proof with no axiom/trust disclosure.
- Treating the repository label `已验证` as source or machine evidence.
