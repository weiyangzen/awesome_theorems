# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `证明复杂性下界`, the attribution
`众多数学家` (many mathematicians), the decade `1980s`, and only `证明长度的下界` ("lower bounds
on proof length") as the statement. Stage0 repeats that wording while leaving precise definitions,
hypotheses, proof process, date of proof, dependencies, equivalent formulations, axioms, and formal
artifacts open. The rev-5.6 manifest retains `已验证` only in the explicitly untrusted
`source_status_untrusted` field.

The neighboring entries do not disambiguate this record. `THM-M-0737` names Frege-system lower
bounds and `THM-M-0738` names extended Frege, so importing either topic here would risk duplicate or
contradictory scope. No author, paper title, immutable edition, theorem number, page, formula family,
proof system, numerical bound, assumptions, or proof passage is supplied.

## Source work required

A later source audit must inspect an immutable primary source and identify one exact proved lower-
bound proposition. It must crosswalk the source's formula language, proof-system rules, hard family,
encoding, proof-size measure, asymptotic quantifiers, theorem/page, assumptions, and errata. It must
also justify why that result, rather than a different proof-system lower bound or an open strong-
system problem, is the intended repository target and obtain independent review.

## Crosswalk

| Repository phrase | Missing mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "proof" | named proof system, rules/verifier, soundness and completeness | source-faithful syntax, verifier/derivation relation, and semantic contract | absent |
| "length" | symbols, lines, clauses, dag/tree size, or encoded bits | exact representation and `Nat`-valued measure invariant under permitted encodings | ambiguous |
| "lower bound" | bound function and ordered asymptotic quantifiers | explicit quantified inequality with all thresholds and parameters | absent |
| many mathematicians, 1980s | broad historical locator | immutable primary edition and pinpoint theorem | not a usable citation |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks list length, finite-set cardinality, ranges, and finite function-space cardinality.
These are only primitive encoding and size vocabulary. A bounded pinned-tree name search found no
Cook-Reckhow, Frege, or proof-complexity API. This observation is not the later immutable formal-
anchor audit and supplies no canonical statement or proof credit.
