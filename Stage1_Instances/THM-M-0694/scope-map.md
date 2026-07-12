# Scope map

## Included topic boundary

- A source-selected natural-deduction calculus with explicit formula syntax and contexts.
- Its exact introduction, elimination, structural, absurdity, and classical rules.
- A source-stated metatheorem or derivability proposition about that calculus.
- Required semantics, substitutions, free-variable conditions, and derivation equivalence.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different targets:

1. A definition of a propositional or first-order natural-deduction derivability judgment.
2. Soundness or completeness with respect to a selected semantics.
3. Normalization, subformula, consistency, or admissibility results.
4. Equivalence with a Hilbert system, sequent calculus, typed lambda calculus, or Lean's ambient
   proposition rules.
5. Derivability of one particular formula from one particular context.

The statement phase must inspect an immutable source and freeze one proposition, including ordered
binders, object logic, syntax representation, context discipline, rule set, semantics, and exact
conclusion. It must decide intuitionistic versus classical logic, weakening/contraction/exchange,
ex-falso, eigenvariable conditions, empty contexts/signatures, and whether derivations are proof
objects or mere propositions.

## Explicit exclusions

- Treating the name of a proof formalism as though it were a proposition.
- Substituting cut elimination, sequent calculus, Curry-Howard, or generic Lean tautologies.
- Defining a custom calculus and proving only a constructor or tautological projection.
- Identifying Lean's metalogic itself with a source-specified natural-deduction calculus.
- Crediting the repository label `已验证` as human-source or machine-proof evidence.
- Reusing the local `S1_M_298.lean` partial calculus as target identity or proof credit; it belongs
  to another theorem and explicitly describes itself as an API choice, not a completeness theorem.

No canonical Lean target is frozen at intake because the source record does not identify one.
