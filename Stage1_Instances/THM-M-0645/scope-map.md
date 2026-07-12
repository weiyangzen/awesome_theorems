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

## Decisions required at statement phase

- Select a primary-source statement and transcribe its formula class, primitive connectives,
  quantifiers, equality convention, and notion of general validity.
- Select a concrete Lean calculus (Hilbert, sequent, or natural deduction), including its finite
  proof object and empty-context derivability judgment. The theorem must not quantify over an
  arbitrary calculus carrying completeness as an assumption.
- Decide whether equality is logical, supplied by an equality theory, or absent. Do not silently
  prove only the equality-free fragment if the chosen source includes equality.
- Freeze the nonempty-domain convention, treatment of empty languages and zero-ary symbols,
  capture-avoiding substitution, universal closure of formulas with free variables, binder order,
  and universe levels.
- Freeze the foundation, TCB, and computation profiles, then mutation-test removal of validity,
  replacement of sentences by open formulas, empty structures, and weakening of the conclusion.

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
