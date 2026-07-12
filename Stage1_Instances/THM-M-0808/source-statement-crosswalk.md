# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `投影集层次`, attributes it only to
"many mathematicians", dates it to the twentieth century, and gives the gloss `投影集的分类`
("classification of projective sets"). Stage0 repeats this metadata while leaving exact
definitions, assumptions, proof path, required axioms, and formal artifacts unresolved. The
rev-5.6 manifest retains `已验证` only in the explicitly untrusted `source_status_untrusted` field.

The source record provides no definition, proposition, hypothesis, conclusion, edition,
theorem/page, proof reference, or formal declaration. Nearby records on analytic sets,
determinacy, and descriptive set theory establish only the subject neighborhood and cannot supply
the missing statement.

## Candidate source work

A standard descriptive-set-theory monograph can locate definitions and classical hierarchy
results, but no edition or pinpoint passage is accepted at intake because the repository has not
identified which result it intends. The source audit must choose the exact result first, then record
an immutable edition or paper revision, theorem/page, definitions, assumptions, proof boundary,
errata, and independent review. Selecting a familiar hierarchy theorem now would be speculation,
not an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "projective sets" | lightface or boldface pointclasses on a coded real/Polish space | sets of reals, codes, parameter convention, and pointclass predicates | convention absent |
| "hierarchy" | finite levels generated from a base using projection and complement | indexed pointclasses and typed closure operations | base and indexing absent |
| "classification" | definition, membership characterization, closure, inclusion, universal-set, separation, uniformization, or strictness result | one concrete proposition with all hypotheses | conclusion absent |
| descriptive-set-theory infrastructure | trees, analytic sets, Polish/Borel spaces | `Descriptive.tree`, `MeasureTheory.AnalyticSet`, `PolishSpace`, `StandardBorelSpace` | pinned APIs probed; ingredients only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports descriptive trees and Polish-space analytic-set infrastructure and checks five
relevant API types. A scoped source-name search found no declaration named for a projective
hierarchy. This is only an environment and feasibility observation; it is not the later immutable
anchor audit and does not establish absence from every namespace or external Lean project.
