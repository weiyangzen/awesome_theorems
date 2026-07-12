# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` records the title `Curry-Howard对应`, attributes it to Haskell
Curry and William Howard, dates it to 1969, and gives only `证明与程序的对应` ("correspondence
between proofs and programs"). `Docs/researches/cs_theorems.md` has a separate computer-science
inventory record with the slogan `命题即类型，证明即程序` ("propositions as types, proofs as
programs") and the broad date 1934-69. `Docs/Stage0_Blueprint.md` explicitly leaves definitions,
assumptions, equivalent formulations, axioms, machine status, and artifact links open.

The rev-5.6 manifest selects only mathematical target `THM-M-0695` and preserves `已验证` as
`source_status_untrusted`. None of these records supplies a source edition, page, formal syntax,
translation, hypotheses, conclusion, proof, or machine declaration.

## Candidate source work

Howard's manuscript commonly published as "The formulae-as-types notion of construction" and
Curry's earlier proof-theory work are candidate primary-source families, but no edition or passage
is accepted at intake. Source audit must identify the exact edition and locator, formal systems,
translation clauses, theorem or metatheoretic claim, assumptions, later corrections, and an
independent reviewer. Historical attribution and a slogan cannot satisfy `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "proposition as type" | translation from formulas/connectives to types/type formers | encoded formula/type syntax or a precisely stated internal interpretation | candidate only |
| "proof as program" | translation from proof derivations to typed terms | encoded derivations, terms, typing, and translation function/relation | candidate only |
| "correspondence" | derivability/inhabitation iff, bijection modulo equality, or step simulation | exact proposition with equality/reduction conventions | absent from source record |
| Curry/Howard, 1969 or 1934-69 | historical attribution | edition, stable section/page, assumption and errata map | unresolved |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib` and checks Lean's `Prop`, logical connective/type constructors, their
introduction/elimination constants, and representative function terms. This confirms encoding
ingredients only. Because Lean itself embodies one propositions-as-types discipline, these checks
must not be mistaken for a syntax translation, adequacy theorem, bijection, or operational
correspondence between independently defined systems. Formal anchor discovery belongs to the later
immutable anchor-audit phase after the exact target is frozen.
