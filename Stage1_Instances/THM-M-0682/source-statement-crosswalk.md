# Source-statement crosswalk

## Available repository source

`Docs/researches/math_theorems.md` gives Ellis Kolchin, 1973, and only "the Galois theory of
differential equations". `Docs/Stage0_Blueprint.md` repeats these facts while leaving definitions,
hypotheses, proof route, axioms, and formal artifacts open. The manifest's `已验证` field is
explicitly untrusted under rev-5.6 and supplies neither a human proof nor kernel evidence.

## Primary-source candidates

- Ellis R. Kolchin, *Differential Algebra and Algebraic Groups*, Pure and Applied Mathematics 54,
  Academic Press, 1973. The author and year match the repository record, so this is the leading
  primary-edition candidate. The record supplies no chapter, theorem, or page, and the relevant
  proposition and errata have not been inspected or independently reviewed here.
- The classical Picard-Vessiot literature is a possible historical source family if the intended
  root is an existence theorem or fundamental correspondence. It is not interchangeable with an
  unspecified Kolchin theorem and has not been selected by intake.

These are bibliographic discovery anchors only. They support a bounded intake classification, not
`H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "differential equations" | linear differential system/module over a differential field | `Differential`, `DifferentialAlgebra`, matrices/modules and a selected equation encoding | differential-field primitives located; equation open |
| "Galois" | differential automorphism group of a Picard-Vessiot extension | differential field extensions, automorphisms commuting with derivation, algebraic groups | no exact local declaration located |
| "theory" | existence/uniqueness, correspondence, fixed fields, or solvability criterion | one exact proposition, not a subject namespace | conclusion open |
| Ellis Kolchin, 1973 | likely bibliographic locator | no formal component or proof credit | matching book candidate only |
| `已验证` | repository status label | none | untrusted and excluded from H/M evidence |

## Lean discovery boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.FieldTheory.Differential.Basic`, including `Differential`, `DifferentialAlgebra`, and
`Differential.uniqueDifferentialAlgebraFiniteDimensional`. It also contains
`Mathlib.FieldTheory.Differential.Liouville`, whose `IsLiouville` notion supports a formalization of
Liouville's theorem about elementary integration. A scoped text and path search found no
Picard-Vessiot definition, differential automorphism group, or fundamental differential Galois
correspondence. The nearby APIs neither determine the source proposition nor close it.

Before `H0`, an independent specialist must approve a stable primary-source theorem/page, its
definitions and assumptions, translation, source boundaries, proof mapping, and errata disposition.
Before statement credit, those reviewed rows must map to one elaborated Lean proposition with
checked transports and mutations. Neither gate is passed at intake.
