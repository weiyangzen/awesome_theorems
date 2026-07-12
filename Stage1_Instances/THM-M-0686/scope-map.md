# Scope map

## Repository claim

The full repository record is the title `超限归纳`, Gerhard Gentzen, 1936, and the gloss
`证明论中的超限归纳` ("transfinite induction in proof theory"). It supplies no exact proposition,
ordinal bound, notation grammar, order relation, predicate class, base theory, quantifier order, or
conclusion. Intake freezes this ambiguity instead of converting a topic into a convenient theorem.

## Candidate theorem families

- The general semantic well-founded induction theorem for a well-founded relation.
- Transfinite induction on actual ordinals, either globally or below a fixed ordinal.
- Induction on a recursive ordinal-notation system below a bound such as epsilon zero, conditional
  on the well-foundedness or descent properties of that notation system.
- An induction schema expressible or provable in a specified arithmetic theory for a specified
  class of formulas.
- The transfinite-induction premise used in Gentzen's consistency proof, together with an explicit
  statement of the theory in which that premise is justified.

These differ in logical strength, foundations, data, and conclusion. They are candidate readings,
not interchangeable encodings and not accepted roots.

## Decisions required before statement freeze

- Inspect and pin a primary edition, exact section/theorem/page, translation, definitions, and
  errata status; obtain independent source review.
- Decide whether the subject is a standalone induction principle or its role in a consistency
  proof. Do not merge this target with the separate `THM-M-0685` Gentzen consistency target.
- Fix actual ordinals versus a recursive notation system, the strict predecessor relation, the
  ordinal bound and endpoint convention, and the proof of well-foundedness credited as an input.
- Fix semantic predicates versus encoded formulas, the formula complexity class, and all parameters.
- Fix the ambient metatheory and object theory, especially whether induction is assumed externally
  or represented internally as an axiom schema or derivability claim.
- Fix ordered binders, universes, classical principles, coding assumptions, and boundary cases.

## Explicit exclusions

- `Ordinal.induction` or `WellFoundedLT.induction` is not adopted merely because it is nearby and
  kernel checked; it is a semantic induction theorem over mathlib ordinals.
- Mathlib's ordinal notation and epsilon-zero APIs do not by themselves formalize a Gentzen-style
  arithmetic theory, formula schema, or consistency argument.
- Ordinary natural-number induction, structural induction on syntax, and Noetherian induction on an
  arbitrary relation are not substituted without a checked relationship to the selected source.
- The repository status label `已验证`, a theorem name, or a successful discovery probe gives no
  source, statement, or proof credit.

## Boundary cases

The statement phase must test the empty and singleton cases, successor and limit stages, bounded
versus unbounded quantification, whether the endpoint is included, and malformed or ill-founded
notation codes. It must decide whether predicates carry parameters and whether the induction step
quantifies over every predecessor or only a fundamental-sequence/notation predecessor relation.
