# Scope map

## Included claim

- An arbitrary indexed family `A i`.
- A nonemptiness witness for every fiber.
- Existence of one simultaneous selector, represented as a dependent function.
- Empty index types, for which the selector exists vacuously.
- Explicit reporting that the Lean closure rests on foundational choice.

## Statement decisions frozen provisionally

- The canonical target uses `iota : Sort u`, `A : iota -> Sort v`, the ordered fiberwise
  nonemptiness hypothesis, and `Nonempty (forall i, A i)`.
- The empty index is included; an empty fiber fails the explicit hypothesis.
- The pointwise binder grouping is checked definitionally. Four required structural mutation
  classes are distinguished by the statement validator.

## Decisions deferred beyond statement freeze

- Transports to set membership, right inverses of surjections, and nonempty products.
- Equivalence audits for well-ordering and Zorn formulations.
- Proof, terminal-body provenance, axiom profile, and release evidence.

## Explicit exclusions

- Countable choice or dependent choice as a broadened or weakened substitute.
- Unique choice, which has different constructive strength.
- The well-ordering theorem or Zorn's lemma without a checked equivalence transport.
- A selector supplied as an extra hypothesis followed by a tautological projection.
- Treating `Classical.choice` as a derived proof with no axiom/trust disclosure.
- Treating the repository label `已验证` as source or machine evidence.
