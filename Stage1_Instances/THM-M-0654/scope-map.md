# Scope map

## Included theorem family

- Two classical first-order theories `T₁` and `T₂` in languages `L₁` and `L₂`.
- A common-language interface, provisionally the intersection language `L₀ = L₁ ∩ L₂` or explicit
  embeddings of one language into the other two.
- Consistency of the combined theory after transporting both theories into a common union language.
- A compatibility condition stated only through common-language sentences: provisionally, there is
  no `L₀`-sentence `φ` for which one theory entails/proves `φ` and the other entails/proves `¬φ`.
- Both directions of the characterization if that biconditional is what the inspected source states.

This is a theorem-family freeze, not an exact statement freeze. Robinson's paper must decide which
of these provisional components and conventions constitute the historical root.

## Decisions reserved for the statement phase

The primary-source audit must fix:

- whether languages are literal symbol-set intersections or signatures with embeddings;
- equality, relation and function symbols, empty sorts/domains, and finitary first-order syntax;
- whether `T₁` and `T₂` include a shared base theory and how theories are transported to the union;
- syntactic consistency (`False` is not derivable), satisfiability, or a proved equivalence between
  them, including every completeness-theorem dependency;
- whether the criterion quantifies over sentences, closed formulas, or common consequences/theories;
- the direction and polarity of the separator, binder order, and use of negation;
- whether separate consistency of `T₁` and `T₂` is assumed or follows from the compatibility clause;
- classical logic, compactness, completeness, and interpolation assumptions used by the proof;
- degenerate cases such as an empty common signature, inconsistent component theory, identical
  languages, and an empty theory.

## Explicit exclusions

- Robinson arithmetic `Q`, Robinson nonstandard analysis, and Robinson's test for stability.
- Mere separate consistency of `T₁` and `T₂`; that does not generally imply consistency of their
  union when they disagree in the common language.
- The adjacent repository item called "joint consistency theorem" as an automatic alias. Its
  provenance and mathematical identity must be audited rather than merged by title.
- A special case with identical languages, disjoint languages, finite theories, or propositional
  theories as a substitute for the source theorem.
- An abstract Lean structure that contains union consistency or the desired equivalence as a field.
- Craig interpolation or first-order completeness alone presented as the target. They may become
  proof obligations only after the canonical source statement is frozen.

## Expected formal surfaces

The exact target will require concrete Lean encodings of signatures and language homomorphisms,
first-order syntax and sentences, theory transport and union, derivability or semantics, negation,
and consistency. Any bridge between derivability and satisfiability must be an explicit checked
node rather than a definitional assumption.
