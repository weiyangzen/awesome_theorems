# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the entry to Saharon Shelah, dates it to 1978, and
states only "an independence concept in stability theory". Stage0 repeats that phrase. Neither
record contains a declarative mathematical claim, definitions, assumptions, a publication title,
theorem number, page, edition, proof, errata, or formal artifact. The manifest deliberately marks
`已验证` as untrusted source metadata.

The attribution and year are not sufficiently precise to identify a theorem. Forking was developed
in Shelah's classification/stability theory, but a historical attribution is not a substitute for
selecting an exact result.

## Candidate primary-source family

Saharon Shelah, *Classification Theory and the Number of Non-Isomorphic Models*, North-Holland,
1978, is the leading primary-source candidate suggested by the repository attribution. No stable
scan or edition has been inspected during this intake, and no chapter, definition, theorem, page,
assumption, or erratum is asserted. Later editions can differ materially in organization and
terminology. This locator therefore supports discovery only, not `H0` or an exact statement.

A source audit must inspect an immutable edition, determine whether the intended target is a single
forking theorem or an independence-calculus package, identify all prerequisite definitions and
cardinal/saturation assumptions, check corrections, and obtain an independent row-by-row review.

## Provisional crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| stable theory | a complete first-order theory satisfying a selected stability condition | `Language.Theory`, completeness, type spaces, cardinal bound | family included; stability API not found |
| type over parameters | complete type of a tuple over a set, often represented using added constants | `Theory.CompleteType`, `withConstants`, restriction maps | partial generic ingredients found |
| dividing | inconsistency along a base-indiscernible sequence | formulas, indiscernibles, consistency, sequences | encoding open; no scoped API found |
| forking | finite-disjunction closure of dividing, then extension to types | formula sets, finite disjunction, complete types | encoding open; no scoped API found |
| independence | `tp(a/B)` does not fork over `A` | tuples, parameter expansions, type restriction, ternary predicate | root relation open |
| independence calculus | invariance, finite character, symmetry, transitivity, extension, local character | separate exact propositions and checked package assembly | candidate conclusion only |
| Shelah / 1978 | historical locator | no Lean object and no proof credit | exact source unresolved |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Types` supplies `Theory.CompleteType`, `Theory.typeOf`, and realized types;
`LanguageMap` supplies languages with constants; and `ElementaryMaps` and
`ElementarySubstructures` supply elementary model maps. `IntakeProbe.lean` checks representative
names against the pinned Lean executable.

A case-insensitive scoped search of `Mathlib/ModelTheory` found no model-theoretic declarations or
files named for forking, nonforking, dividing, indiscernibles, or stability. Probability files with
"independence" are unrelated and excluded. This is negative intake evidence, not the required
immutable external-anchor audit, and no candidate receives proof credit.
