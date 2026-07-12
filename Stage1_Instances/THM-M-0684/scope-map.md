# Scope map

## Included topic boundary

- A source-specified effectively axiomatized formal theory `T` and exact arithmetic-strength
  assumptions.
- A source-specified coding of syntax and proof, arithmetized provability predicate `Prov_T`, and
  consistency sentence `Con(T)`.
- The precise derivability/representability hypotheses used by the selected formulation.
- The exact internal or external unprovability conclusion and the metatheory asserting it.

## Choices required at statement freeze

The repository gloss does not determine:

1. whether the target is specifically PA, any recursively enumerable consistent extension of a
   weak arithmetic base, or another class of theories;
2. whether simple consistency, omega-consistency, or another soundness condition is assumed;
3. which proof calculus, Godel numbering, proof predicate, and internal consistency sentence are
   used;
4. whether the conclusion is the metatheoretic `T does not prove Con(T)`, an internal conditional,
   or a uniformly quantified theorem over theories;
5. the base metatheory and any standard-model or soundness assumptions.

These choices affect the proposition and cannot be treated as interchangeable implementation
details. The statement phase must select an immutable source passage, freeze all ordered binders
and hypotheses, and justify checked transports for any alternate formulation.

## Explicit exclusions

- The first incompleteness theorem as a substitute.
- A theorem merely saying that some sentence is unprovable, without identifying `Con(T)`.
- Consistency proofs in a stronger metatheory, such as a Gentzen-style relative proof, as the root
  claim; they do not say that `T` proves its own consistency.
- Inconsistent or insufficiently strong theories hidden under an unrestricted word "system".
- A generic modal-logic slogan or abstract derivability theorem without a checked bridge to the
  selected arithmetical theory.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record leaves every root-critical
formal parameter above unspecified.
