# Scope map

## Included topic boundary

- A source-selected lambda-calculus syntax, including the binding representation and equality of
  terms.
- A source-selected operational relation such as beta reduction and its reflexive-transitive
  closure, if it occurs in the exact proposition.
- One concrete theorem or characterization, with every binder, hypothesis, and conclusion taken
  from an immutable source passage.
- The exact typed or untyped setting and any restrictions to open, closed, normal, or typable terms.

## Ambiguities to resolve at statement freeze

The repository record does not distinguish among materially different targets:

1. the definition or construction of the untyped lambda calculus as a computation formalism;
2. a syntactic metatheorem about free variables, renaming, substitution, or alpha-equivalence;
3. beta-reduction confluence, standardization, solvability, or another untyped metatheorem;
4. normalization, progress, preservation, or consistency for a specified typed lambda calculus;
5. a representation or expressiveness result for computable functions;
6. equivalence with Turing machines or another computation model.

The statement phase must select a proposition rather than merely encode a datatype. It must freeze
named variables versus de Bruijn indices, alpha-quotiented versus raw syntax, capture-avoiding
substitution, beta versus beta-eta conversion, one-step versus multi-step reduction, reduction
under binders, typed versus untyped terms, and all boundary cases.

## Explicit exclusions

- `THM-M-0705`, the separately listed Church-Rosser confluence theorem, as a silent substitute.
- `THM-C-0021`, the separately listed lambda-calculus/Turing-machine equivalence result, as a
  silent substitute.
- Lean's own dependent function terms or kernel reduction as proof of a theorem about a separately
  defined object language.
- Simply typed, polymorphic, linear, probabilistic, or dependent lambda calculi unless the selected
  source explicitly chooses that calculus.
- A datatype definition, evaluator example, or assumed relation packaged as a tautological theorem.
- The inventory label `verified` as evidence for either a human proof or kernel closure.

No canonical Lean target is frozen at intake because the repository record identifies no unique
proposition.
