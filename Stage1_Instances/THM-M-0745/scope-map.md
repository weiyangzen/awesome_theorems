# Scope map

## Received scope

The repository fixes the title "recursively enumerable sets" and the open-ended phrase
"properties of recursively enumerable sets." Stage0 explicitly leaves the precise definitions,
premises, proof route, dependencies, equivalent formulations, axioms, machine state, and artifact
links pending. This establishes a recursion-theory topic boundary but no ordered binders,
hypotheses, or conclusion.

## Proposition families not selected

An admitted source correction might select one of the following, but intake credits none as the
root:

- a definition or characterization by the domain of a partial recursive function;
- a characterization as the range of a total computable enumeration, with a convention for the
  empty set;
- equivalence between semidecidability, enumerability, and machine recognizability;
- closure under union, intersection, computable preimage, image, or existential projection;
- the fact that every computable predicate is recursively enumerable;
- the characterization of computable predicates as both r.e. and co-r.e.;
- recursive enumerability of the halting predicate or a completeness theorem for it; or
- a theorem about creative sets, simple sets, many-one degrees, c.e. degrees, or Diophantine sets.

These statements are not interchangeable. Some are definitions, some are equivalences, some need
decidability or coding assumptions, some concern only examples, and some are substantial later
theorems.

## Decisions required at statement freeze

1. Admit an immutable primary or authoritative source and one exact theorem, definition-plus-result,
   section, page, or formula, including proof boundary, corrections, errata, and independent review.
2. Fix the carrier: predicates or sets over natural numbers, positive integers, program codes, or
   an arbitrary `Primcodable` type, together with universe and encoding assumptions.
3. Fix the computational model: partial-recursive domain, computable enumerator or range,
   semidecision procedure, Turing-machine recognizer, or a checked equivalent presentation.
4. Choose one exact property or characterization and freeze every ordered binder, explicit and
   implicit hypothesis, conclusion, and direction of implication.
5. Decide whether an enumerator must be total, whether repetitions are allowed, and how the empty
   set is represented.
6. Decide whether predicates carry a `DecidablePred` instance and where classical logic,
   extensionality, choice, quotients, and coding infrastructure enter.
7. Resolve empty, finite, universal, decidable, nondecidable, singleton, complement, and malformed-
   code cases under the selected formulation.
8. Compile checked transports for every credited predicate/set, domain/range, semidecision, or
   recognizer encoding, then mutation-test assumptions, domain, binder scope, and boundary cases.

## Neighbor boundaries

- `THM-M-0741` separately owns the halting-problem target. Its r.e. predicate may be an example or
  dependency, not this unspecified root.
- `THM-M-0746` and `THM-M-0747` separately own creative-set and simple-set results.
- `THM-M-0748` separately owns Post's problem, and `THM-M-0758` separately owns computably
  enumerable degrees.
- `THM-M-0714` separately owns the MRDP statement that recursively enumerable sets are
  Diophantine.

No source, statement, proof body, or receipt credit transfers across these boundaries.

## Explicit exclusions

- Do not select `ComputablePred.to_re`, `computable_iff_re_compl_re`, or
  `halting_problem_re` merely because a convenient pinned declaration exists.
- Do not replace the root with the definition of `REPred` or a tautological restatement of that
  definition unless an accepted source explicitly chooses a characterization theorem and its exact
  directions.
- Do not broaden from natural-number sets to arbitrary encodable types, or specialize in the other
  direction, without a source-approved statement and checked transport.
- Do not substitute a closure theorem, completeness theorem, creative/simple-set theorem, degree
  theorem, MRDP, Rice theorem, or s-m-n theorem for the generic word "properties."
- Do not encode the missing result as an axiom, opaque predicate, assumed certificate, or structure
  field from which the desired conclusion is projected.
- Do not treat `已验证`, a bibliography entry, an API name, or a successful probe as source or
  theorem evidence.

## Lean boundary and retry condition

Pinned mathlib defines `REPred p` through the domain of a computable partial function and proves
several distinct adjacent results. The probe authenticates those interfaces only. Minimal imports,
a canonical expression, expression and environment fingerprints, transports, statement mutations,
and proof-body provenance remain downstream.

The integration lane must first admit one stable proposition and immutable source, then obtain an
independent review of its definitions, binders, assumptions, conclusion, proof boundary,
corrections, errata, translation, and relationship to the catalog phrase. Only then may the
statement phase elaborate and mutation-test an exact target.
