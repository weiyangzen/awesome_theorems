# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` supplies only the Chinese heading "quantifier elimination", the
attribution "many mathematicians", the period "20th century", and the sentence "quantifier
elimination for a theory". Stage0 repeats that sentence. Neither record names a theory, gives a
theorem locator, states hypotheses or a conclusion, or cites a proof. The manifest preserves the
label `已验证` as explicitly untrusted metadata.

The adjacent inventory rows separately name Tarski quantifier elimination for real closed fields
and Ackermann quantifier elimination for Presburger arithmetic. That separation is evidence against
silently interpreting this generic row as either concrete theorem, but it does not identify a third
root proposition.

## Candidate references

Standard model-theory texts such as C. C. Chang and H. J. Keisler, *Model Theory*, and Wilfrid
Hodges, *Model Theory*, are candidate references for the definition and general characterizations
of quantifier elimination. Exact editions, sections, theorem/page locators, assumptions, and errata
have not been inspected for this intake. They are discovery directions only, not `H0` evidence and
not evidence that the repository intended a particular characterization theorem.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "a theory" | one fixed first-order theory `T` | `FirstOrder.Language.Theory` | theory identity absent |
| "quantifier" | `forall`/`exists` binders in formulas | `Language.BoundedFormula` binders | pinned syntax available |
| "quantifier-free" | Boolean combinations of atomic formulas | `Language.BoundedFormula.IsQF` | pinned predicate checked |
| "elimination" | existence of a same-context quantifier-free equivalent | existential formula plus semantic or provable equivalence | exact relation open |
| modulo `T` | equivalence in every model of the theory | model satisfaction and realization under assignments | encoding open |
| theorem claim | a concrete `T` has QE, or a characterization theorem | exact proposition with hypotheses and conclusion | absent from source record |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Complexity` defines `BoundedFormula.IsQF` and proves that every formula has an
equivalent prenex form via `realize_toPrenex`. `IntakeProbe.lean` checks these interfaces using the
pinned Lean executable. Prenex normalization retains quantifiers and therefore supplies no proof
of quantifier elimination. The Presburger module explicitly lists quantifier elimination as a
TODO, which likewise receives no closure credit.

Before `H0`, a primary proof source for one exact proposition must be selected, pinpointed, checked
for assumptions and errata, mapped row by row, and independently reviewed. Before statement credit,
that proposition must map to an elaborated Lean target without inserting a theory, weakening
uniform model equivalence, or replacing elimination with prenex normalization.
