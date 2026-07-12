# Scope map

## Provisional included claim

- A source-specified effectively axiomatized theory `T` in a fixed language and deductive calculus.
- A specified arithmetic-strength or interpretability threshold sufficient to arithmetize syntax.
- A represented proof predicate and internal provability predicate satisfying every derivability
  condition actually used by the chosen formulation.
- The canonical internal consistency sentence, provisionally `not Provable_T(false)`.
- A metatheoretic implication from consistency of `T` to non-derivability in `T` of that sentence.

## Decisions required at statement freeze

1. Inspect and select an exact theorem in an immutable primary source or a precisely identified
   modern formulation; record theorem/page, definitions, assumptions, translation, and errata.
2. Fix `T`, its language, axioms, proof calculus, effective presentation, arithmetic base, and
   whether extension or interpretation of that base is required.
3. Separate external consistency of `T` from the formula inside `T` expressing consistency, and
   define both without assuming their desired relationship.
4. Fix the proof-coding and provability predicate and state the Hilbert-Bernays-Lob derivability
   conditions or source-specific representability lemmas rather than hiding them in a typeclass.
5. Freeze ordered binders, universes, classical or constructive metatheory, induction principles,
   and any soundness or standard-model assumptions.
6. Map the selected proof route, such as derivation from the first incompleteness theorem or Lob's
   theorem, without substituting either related theorem for this target.

## Explicit exclusions

- Godel's first incompleteness theorem (`THM-M-0777`) as the target, though it may be a dependency.
- Lob's theorem, Tarski undefinability, Church undecidability, or a modal provability-logic result as
  a substitute rather than a source-mapped route to the exact conclusion.
- The false universal reading covering every consistent formal system, including theories too weak
  to express arithmetic or their own proof relation.
- Defining `Con(T)` as an arbitrary proposition chosen to make non-provability immediate.
- Assuming the target non-provability, a Godel sentence, or all derivability conditions as one
  opaque premise and then calling the wrapper the second incompleteness theorem.
- Treating generic syntax, the beta-function coding lemma, or `已验证` metadata as proof credit.

No canonical Lean target is frozen at intake; the missing choices change both hypotheses and the
conclusion and cannot be filled by convenience.
