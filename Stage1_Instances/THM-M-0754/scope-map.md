# Scope map

## Preserved topic boundary

The source label concerns the arithmetical hierarchy of predicates, relations, or sets over a
source-selected arithmetic domain. A later source and statement freeze must make all of the
following explicit:

- the object classified: subsets of `Nat`, finitary relations on `Nat`, formulas, indices, or
  another source-defined coding;
- the first-order language and intended structure, including which arithmetic functions and
  relations are primitive and which are merely definable;
- the base/level-zero convention and the indexing origin for `Sigma^0_n`, `Pi^0_n`, and
  `Delta^0_n`;
- whether the hierarchy is defined syntactically by alternating unbounded quantifiers,
  semantically by definability in the standard model, computationally by oracle jumps, or through
  checked equivalences among these presentations;
- whether number parameters are allowed, how tuples are coded, and whether bounded quantifiers
  count toward alternation depth; and
- the exact truth-valued conclusion and every required hypothesis.

This inventory preserves a topic family. It is not a canonical proposition, Lean target, or proof
architecture.

## Decisions required at statement freeze

1. Acquire and independently review an immutable primary or approved authoritative source, with
   exact edition, theorem/definition and page or section, incorporated definitions, assumptions,
   conclusion, proof boundary, corrections, and errata.
2. Decide whether the scheduled root is a definition package or a particular theorem. A definition
   alone cannot be reported as a proved proposition merely because the catalog calls every row a
   theorem candidate.
3. If a theorem is selected, freeze its direction and strength: closure, normal form,
   computability/relative-computability characterization, completeness, strictness, properness,
   non-collapse, or another result are not interchangeable.
4. Fix the arithmetic structure and formula syntax, free-variable and parameter conventions,
   quantifier polarity and block conventions, bounded-quantifier treatment, level-zero class, and
   encodings of tuples and sets.
5. Freeze ordered binders, hypotheses, conclusion, foundation and TCB profiles, minimal imports,
   expression/environment fingerprints, alternate encodings, checked transports, and all four
   required statement mutations.
6. Resolve boundary cases including level zero, empty/full sets, zero-arity predicates, formulas
   with no unbounded quantifiers, complement/dual conventions, vacuous quantifier blocks,
   nonstandard models, and parameter-free versus parameter-allowing definitions.

## Explicit exclusions

- Choosing strictness or non-collapse of the hierarchy merely because it is a familiar theorem.
- Choosing a completeness theorem, Post theorem, normal-form theorem, closure theorem, or
  definability/computability equivalence without a source decision.
- Replacing the target with the analytical, hyperarithmetical, polynomial, exponential, space, or
  Chomsky hierarchy.
- Using Presburger quantifier elimination, a generic prenex-normal-form theorem, primitive
  recursion, the halting theorem, or Turing-jump machinery as the target rather than possible
  ingredients.
- Encoding arbitrary propositions into artificial `Sigma`/`Pi` labels or storing the desired
  classification or separation result as a structure field or hypothesis.
- Crediting a finite-level example, bounded computation, search result, catalog status, theorem
  name, unpinned external repository, placeholder, axiom, or oracle as source or proof evidence.

No canonical statement, formal expression, alternate transport, obligation registry, discovery
protocol, accepted proof state, or completion claim is frozen at intake.
