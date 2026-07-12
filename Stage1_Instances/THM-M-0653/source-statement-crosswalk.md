# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the theorem to Evert Beth, dates it to 1953, and gives
only the sentence "implicit definability and explicit definability are equivalent". Stage0 repeats
that gloss without definitions or assumptions. The manifest preserves `已验证` as explicitly
untrusted metadata. None of these records identifies a proof, theorem number, page, edition, or
formal artifact.

## Candidate primary and reference sources

- Evert W. Beth, *The Foundations of Mathematics: A Study in the Philosophy of Science*, North-
  Holland (1959), is a historical monograph candidate associated with the definability theorem.
  The exact edition, section, theorem/page, formulation, and corrections have not been inspected.
- Evert W. Beth's early-1950s papers on semantic entailment and definability are historical primary
  candidates, but the repository's exact 1953 attribution has not been verified against an
  immutable bibliography or scan.
- Standard model-theory texts present Beth definability as a consequence of Craig interpolation.
  They are useful secondary locators, not primary `H0` evidence.

These are discovery anchors only. The source audit must identify and inspect an immutable primary
text, verify attribution and date, record exact theorem/page and definitions, audit errata, and
obtain an independent row-by-row review.

## Crosswalk

| Repository phrase | Frozen mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| implicit definability | uniqueness of the interpretation of `R` among `T`-models with one fixed `L`-reduct | two expanded structures, `Theory.Model`, reduct equality, equality of relation maps | included; encoding open |
| explicit definability | one old-language formula uniformly defines `R` in all `T`-models | `L.Formula (Fin n)` and realization in the reduct | included; encoding open |
| equivalence | explicit implies implicit and Beth's nontrivial implicit-to-explicit implication | `Iff` or checked assembly of two implications | included; root shape open |
| relative to a theory | every relevant expansion is a model of the same expanded-language `T` | expanded `Language.Theory` and semantic model predicate | pinned ingredients exist |
| old versus expanded language | the defining formula cannot mention `R` | language homomorphism, reduct, and formula mapping | pinned ingredients exist; one-symbol extension open |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.LanguageMap` provides language homomorphisms, reduct structures, and
`IsExpansionOn`; `Mathlib.ModelTheory.Semantics` provides theories and model satisfaction; and
`Mathlib.ModelTheory.Definability` provides formula-based definability of sets and transport to an
expansion. `IntakeProbe.lean` checks these names and types with the pinned Lean executable.

The scoped repository and mathlib search found no declaration named for Beth and no ready-made
notion of implicit definability modulo a theory. This negative search is not a complete anchor
audit. In particular, mathlib's `Set.Definable` concerns a set in one structure and does not by
itself express the uniform all-model conclusion. No candidate receives proof credit at intake.
