# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Wilhelm Ackermann, gives the year 1928, and states only
"quantifier elimination for Presburger arithmetic". `Docs/Stage0_Blueprint.md` repeats that phrase.
The rev-5.6 manifest deliberately preserves `已验证` as untrusted metadata. None gives a title,
edition, theorem or page, definitions of the language, assumptions, proof, errata, or formal
artifact. The nearby naming also risks conflating an Ackermann elimination method with Presburger's
1929 publication; attribution and date therefore remain audit questions rather than frozen facts.

## Candidate source boundary

- Wilhelm Ackermann's 1928 work is the historical-primary-source lead implied by repository
  metadata. Its exact bibliographic identity, statement, page, syntax, and relationship to the
  modern phrase "Presburger arithmetic" have not been inspected in an immutable edition.
- Mojzesz Presburger's 1929 completeness/decidability work is a necessary historical comparison
  source. It must not silently replace the repository's Ackermann attribution.
- Modern logic texts commonly obtain quantifier elimination after expanding the additive language
  with order and congruence predicates. They can clarify terminology but are secondary locators,
  not `H0` evidence for an attribution-specific target.

These are discovery leads only. `H0` requires an inspected primary edition, exact theorem/page,
assumption and notation mapping, errata check, and independent row-by-row review.

## Crosswalk

| Repository phrase | Bounded meaning at intake | Required Lean component | Intake status |
|---|---|---|---|
| Presburger arithmetic | first-order arithmetic of natural-number addition | a frozen language and its standard `Nat` structure or theory | bare mathlib language located; exact expansion open |
| quantifier elimination | every formula has an assignment-uniform quantifier-free equivalent | formula syntax, `IsQF`, realization, and equivalence | APIs located; root shape open |
| Ackermann | attribution to a particular elimination theorem or procedure | source-specific algorithm/specification and correctness target if applicable | primary work not pinpointed |
| verified | repository metadata label only | node-specific kernel and source receipts | no credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Arithmetic.Presburger.Basic` defines the relation-free language `(0,1,+)` and
its standard structure. `Mathlib.ModelTheory.Complexity` defines
`FirstOrder.Language.BoundedFormula.IsQF`. The Presburger definability module proves
`FirstOrder.Language.presburger.definable_iff_isSemilinearSet` over `Nat` and explicitly describes
that semantic characterization, not a quantifier-elimination theorem. The Basic module's TODO says
the theory and its quantifier elimination/completeness remain to be defined and proved.

`IntakeProbe.lean` checks these pinned declarations. A bounded `rg` search of pinned mathlib found
the Presburger modules and the TODO but no terminal Presburger quantifier-elimination declaration.
That negative result is not a complete anchor audit and grants no proof credit.
