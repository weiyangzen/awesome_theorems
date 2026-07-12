# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the name, attribution to Leopold Loewenheim and Thoralf
Skolem, year 1915, and the sentence "无穷模型有任意大的初等等价模型" (infinite models have
arbitrarily large elementarily equivalent models). The same wording is projected into Stage0.
This metadata is the exact intake wording, but its `已验证` label is explicitly untrusted under
rev-5.6 and is not source or machine evidence.

## Candidate sources

- Leopold Loewenheim, *Uber Moglichkeiten im Relativkalkul*, Mathematische Annalen 76 (1915),
  447-470. This is the historical attribution candidate. Its exact theorem, assumptions, original
  logical formalism, and relationship to the modern upward formulation have not been independently
  inspected, so it is not `H0` evidence.
- Thoralf Skolem's later countable-model refinements are required historical comparison sources,
  but an exact edition and theorem/page have not yet been selected. They must not be cited as if
  they directly state the upward elementary-extension claim.
- `Mathlib.ModelTheory.Satisfiability` at mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` documents and declares the modern Upward
  Loewenheim-Skolem theorem `FirstOrder.Language.exists_elementaryEmbedding_card_eq`. This is a
  formal-source candidate, not a primary human-source substitute; its exact type must be audited in
  the statement and anchor-audit phases.
- The same pinned module declares
  `FirstOrder.Language.exists_elementarilyEquivalent_card_eq`, whose conclusion directly matches
  the repository's elementary-equivalence wording. Its hypotheses allow every infinite target
  cardinal at least as large as the language; the intended "arbitrarily large" specialization and
  any added `#M <= kappa` bound must be made explicit rather than silently inserted.
- `Mathlib.ModelTheory.Skolem` at the same revision declares the distinct downward theorem
  `FirstOrder.Language.exists_elementarySubstructure_card_eq`. It is a scope-disambiguation anchor,
  not evidence for the upward target.

## Crosswalk

| Repository component | Intake interpretation | Candidate Lean component | Status |
|---|---|---|---|
| "infinite model" | an infinite `L`-structure `M` | `[Infinite M]` with `[L.Structure M]` | included; exact binders open |
| "arbitrarily large" | every target `kappa` above `#M`, `L.card`, and infinitude bounds | cardinal hypotheses and exact output cardinality | included; lift conventions open |
| "models" | concrete output `L`-structures | existential carrier plus structure | included; packaging open |
| "elementarily equivalent" | same first-order sentences as `M` | `exists_elementarilyEquivalent_card_eq`, or elementary extension plus a checked bridge | included; presentation open |
| Loewenheim-Skolem name/year | historical provenance | no Lean component | attribution does not yet match the modern upward wording |

Before `H0`, a qualified independent reviewer must inspect stable editions, identify exact theorem
locators, map every assumption and conclusion, check translations and errata, and explain the
historical-to-modern theorem-name boundary. Before statement acceptance, Lean must elaborate the
selected expression and a checked bridge from elementary extension to elementary equivalence.
