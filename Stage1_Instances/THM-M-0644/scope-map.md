# Scope map

## Included claim

- Classical compactness for arbitrary first-order languages and arbitrary sets `T` of sentences.
- `T` has a model exactly when every finite subtheory of `T` has a model.
- A model has a nonempty carrier and interprets all symbols of the same language.
- The reverse implication is the substantive compactness direction; the forward implication is
  restriction of a model to a subtheory.
- Empty theories, empty finite subtheories, infinite languages, and infinite theories remain in
  scope. No countability hypothesis is present in the repository wording.

## Formal scope candidate

The pinned candidate represents a theory as `L.Theory`, satisfiability as a nonempty bundled model,
and finite satisfiability by quantifying over `Finset L.Sentence` whose coercion to a theory is
contained in `T`. This matches the repository phrase component by component, subject to the
statement phase serializing the exact expression and independently checking its encoding choices.

## Statement-phase decisions

The next phase must freeze universe levels, implicit binder order, the precise nonempty-model
semantics, and whether the human phrase "every finite subset" is canonicalized directly to
mathlib's `Finset` definition or accompanied by a checked `Set.Finite` transport. It must also
fingerprint the environment and expression and mutation-test removed containment, a changed
sentence domain, changed binder scope, and boundary cases such as the empty theory.

## Explicit exclusions

- Topological compactness, propositional compactness, compactness for infinitary logics, and finite
  model compactness.
- The completeness theorem, even if used to prove an alternate compactness formulation.
- Replacing semantic satisfiability by syntactic consistency without a checked completeness bridge.
- Adding countability, a finite language, or a fixed model universe merely to simplify the target.
- Treating the Stage0 label `已验证`, this intake probe, or an upstream theorem name as accepted
  source or proof evidence.
