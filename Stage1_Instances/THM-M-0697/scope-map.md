# Scope map

## Included theorem family

- First-order languages, formulas/sentences, structures, and satisfaction.
- A theory `T` and semantic consequence of a sentence `phi` from `T`.
- A source-selected finitary proof calculus with an explicit derivability judgment.
- The completeness direction from semantic validity/consequence to formal derivability.
- Any syntax coding, consistency, maximal-theory, Henkin, term-model, or compactness bridges
  actually required by the selected statement and proof route.

## Proposition-changing choices

| Surface | Choices still requiring a source decision |
|---|---|
| Root form | validity implies provability; consequence implies derivability; consistent theory has a model |
| Proof system | Hilbert calculus, natural deduction, sequent calculus, or another explicitly equivalent calculus |
| Premises | empty theory, finite contexts, arbitrary sets of sentences, or arbitrary formulas with free variables |
| Logic | classical versus intuitionistic; equality logical or nonlogical; function and relation signatures |
| Semantics | nonempty structures, assignments for free variables, sentence satisfaction, and universe bounds |
| Consistency | absence of a contradiction, non-derivability of falsity, or syntactic nontriviality |
| Foundation | classical choice, maximal consistent extensions, term-model quotient, and countability assumptions |

## Explicit exclusions

- Soundness (`derivable` implies `semantically valid`) as a substitute for completeness.
- The first-order compactness theorem as the root, even though it is closely related and present in
  pinned mathlib.
- Completeness of a particular theory, such as algebraically closed fields or Presburger arithmetic.
- Propositional completeness, second-order completeness, Gödel incompleteness, or categorical
  completeness.
- A theorem whose desired derivability conclusion is assumed as a hypothesis.
- The catalog label `已验证` or an elaborating API probe as human or kernel proof evidence.

## Statement-phase exit condition

The next phase must inspect an immutable primary source, select an exact theorem and calculus,
freeze every binder and boundary above, and justify the mapping from the catalog title. It must
then define or pin the derivability relation, elaborate the exact Lean proposition, fingerprint it,
and run the four required mutation classes. Until then no canonical formal target exists.
