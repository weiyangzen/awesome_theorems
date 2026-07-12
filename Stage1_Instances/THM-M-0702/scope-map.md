# Scope map

## Included topic boundary

- First-order terms over a source-specified signature and variable type.
- Finite unification problems, represented either by two terms or a finite equation system.
- Substitutions, their action on terms, composition convention, and the relation "is a unifier".
- A specified Robinson-style algorithm including the occurs check and success/failure behavior.
- The exact selected correctness properties: termination, soundness, completeness, failure
  correctness, and/or production of a most general unifier.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different roots:

1. **Soundness:** a substitution returned by the algorithm unifies the input.
2. **Success completeness:** if a unifier exists, the algorithm succeeds.
3. **Failure correctness:** failure implies that no unifier exists.
4. **Most-generality:** every other unifier factors through the returned substitution, under a
   fixed orientation of substitution composition.
5. **Termination and total correctness:** a particular transition system or recursive program
   terminates on every finite input and satisfies some or all of the preceding properties.

The statement phase must inspect an immutable source and freeze one proposition (or one explicitly
bundled theorem), ordered binders, algorithm, input representation, factorization direction, and
equality conventions. It must decide the occurs check, cyclic terms, finite support, variable
renaming, empty problems, and whether syntactic equality or equality modulo an equational theory is
intended.

## Explicit exclusions

- Lean elaborator metavariable unification as a substitute for the first-order term algorithm.
- Higher-order, typed, AC, E-, rational-tree, or semantic unification unless the selected source
  explicitly requires it.
- A theorem merely asserting that some unifier exists, without the named algorithm.
- A function returning a candidate substitution followed by correctness assumed as an argument.
- Any convenient substitution identity absent a checked source crosswalk.
- The repository label `已验证` as evidence of a human proof or machine closure.

No canonical Lean target is frozen at intake because the source record is not proposition-level.
