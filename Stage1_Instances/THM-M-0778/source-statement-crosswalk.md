# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives only the title, Kurt Godel, 1931, and the sentence
`一致形式系统不能证明自身一致性` ("a consistent formal system cannot prove its own consistency").
Stage0 repeats it while leaving exact definitions, premises, foundation, proof route, dependencies,
axioms, and machine artifacts open. The manifest deliberately calls `已验证` an untrusted source
status. These records supply no theorem number, page, edition, translation, or errata record.

## Candidate primary source

Kurt Godel, "Uber formal unentscheidbare Satze der Principia Mathematica und verwandter Systeme I",
*Monatshefte fur Mathematik und Physik* 38 (1931), 173-198, is the historical primary-source
candidate. The statement phase must inspect an immutable edition and identify the exact passage and
formulation. A modern derivability-condition formulation may be chosen only with its own pinpoint
source and an explicit relationship to the historical result. This locator is not `H0` evidence.

## Crosswalk

| Repository phrase | Mathematical choice still required | Required Lean component | Intake status |
|---|---|---|---|
| "formal system" | effective theory, language, axioms, calculus | encoded syntax, theory, proof predicate | absent |
| "consistent" | external absence of a proof of contradiction | metatheoretic consistency predicate | exact form open |
| "its own consistency" | internal arithmetical sentence representing that predicate | coded falsum, provability predicate, `Con_T` formula | absent |
| "cannot prove" | nonexistence of a derivation in the selected calculus | syntactic derivability/non-provability relation | absent |
| unstated strength | sufficient arithmetic and representability hypotheses | arithmetic interpretation and coding lemmas | absent |
| unstated proof conditions | exact derivability/diagonalization conditions | separately named obligations | absent |
| `1931 / Godel` | exact theorem, wording, and assumptions | source-node provenance only | candidate identified |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe checks
`FirstOrder.Language.Theory`, formula syntax, `Nat.beta`, `Nat.unbeta`, and
`Nat.beta_unbeta_coe`. These are generic syntax and finite-sequence coding ingredients. Scoped
repository and pinned-mathlib searches found no second-incompleteness, arithmetized-provability, or
derivability-condition declaration. That bounded negative result is not the later immutable anchor
audit, and the checked ingredients receive no target or proof credit.

Before statement credit, an independent source reviewer must approve the exact source formulation
and every row must map to one elaborated Lean expression. Before `H0`, the complete source proof and
assumption-to-node crosswalk must receive independent review.
