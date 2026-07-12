# Scope map

## Included topic boundary

- A source-specified simple type theory or simply typed calculus.
- Its exact base types, type constructors, terms, contexts, judgments, conversion rules, and logic.
- One exact source assertion about that system, including every hypothesis and semantic convention.
- A Lean 4 encoding and proof of that assertion, rather than use of Lean's own type checker as a
  substitute for a formalized object theory.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different objects or claims:

1. Church's 1940 simple theory of types as a formulation of higher-order logic.
2. A simply typed lambda calculus with arrow types, possibly products, sums, constants, or base
   types, together with its typing and reduction judgments.
3. A classical extensional simple type theory, an intuitionistic variant, or only its syntax.
4. A metatheorem such as weakening/substitution, subject reduction, progress, normalization,
   confluence, consistency, soundness, completeness, or decidability of type checking.

The statement phase must inspect an immutable source and freeze one proposition. It must fix the
object/metatheory distinction, ordered binders, type and term syntax, contexts, equality/reduction,
semantics, logical axioms, and conclusion. It must also decide whether terms are open or closed,
whether signatures can be empty, and whether eta conversion, functional extensionality, choice, or
excluded middle belongs to the object theory.

## Explicit exclusions

- Treating a definition or formal system as though it were a theorem.
- Proving a convenient fact about Lean's native dependent type theory instead of the selected
  simple object theory.
- Substituting Curry-Howard, System F, Martin-Lof type theory, dependent type theory, homotopy type
  theory, or a generic lambda-calculus theorem.
- Assuming a typing derivation or normalization certificate and returning it unchanged.
- Using the repository label `已验证` as evidence of a human proof or kernel closure.
- Selecting a soundness, normalization, or decidability statement absent a pinpoint source.

No canonical Lean target is frozen at intake because the repository source does not assert a
unique proposition.
