# Scope map

## Included claim

The repository phrase `逻辑有效式可证` is read as the validity form of the completeness theorem
for classical first-order predicate logic:

- the domain is an arbitrary first-order language;
- the object is a closed formula (sentence) of that language;
- validity means truth in every nonempty structure interpreting the language; and
- the conclusion is a finite derivation of that sentence from the empty theory/context in a fixed
  classical first-order proof calculus.

This is weak completeness. Strong completeness for an arbitrary theory `T` is a candidate alternate
encoding, not the canonical claim at intake. It may be credited only through checked specialization
to `T = empty` and, in the reverse direction, the hypotheses needed for a deduction/compactness
transport.

## Statement decisions frozen

- Use mathlib `Language`, locally nameless formulas, sentences, semantic realization, and logical
  equality, with model carrier `Type (max u v)` and an explicit `Nonempty` premise.
- Use the inductive finite classical natural-deduction calculus in `Statement.lean`; its rules do
  not contain or assume semantic completeness.
- Quantify the language before the sentence, require semantic validity, and conclude an inhabited
  empty-context derivation. Open formulas are excluded rather than silently universally closed.
- Include empty languages and zero-ary symbols. The checked empty-language boundary and four
  structural mutations are recorded in `statement.json`.

Pinpoint primary-source conventions remain source-audit work. They may require a checked transport
or statement revision; they do not prevent this exact repository-gloss encoding from elaborating.

## Expected semantic and syntactic interfaces

The semantic side needs structures, valuations, realization of formulas, and validity over every
nonempty model. The syntactic side needs an inductive derivation relation whose terminal value is
the target sentence, plus verified soundness. A standard completeness architecture may use
consistent extensions, maximal consistent/Henkin theories, term models, a truth lemma, and a
contrapositive step, but intake does not freeze that proof route or count any of those as closed.

## Explicit exclusions

- Propositional completeness, higher-order completeness, or completeness of intuitionistic logic.
- Model-theoretic completeness of one theory, such as dense linear orders or algebraically closed
  fields.
- Goedel's first or second incompleteness theorem.
- Compactness alone, soundness alone, or the semantic statement that a theory implies a sentence.
- A special finite language/formula fragment, or a single tautology, substituted for arbitrary
  first-order validity.
- A structure, typeclass, axiom, or hypothesis that stores `Valid phi -> Provable phi`.
- Lean's ambient proof of a translated proposition without a represented object-logic derivation.

No degenerate language or vacuous model class may be used to obtain proof credit for the general
root.
