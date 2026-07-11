# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the title "paracomposition",
attribution "Jean-Michel Bony", year 1981, statement "复合函数的仿微分",
importance "high", and the untrusted status `已验证`.
`Docs/Stage0_Blueprint.md` repeats these fields while explicitly leaving exact
definitions, hypotheses, proof, dependencies, axioms, and machine artifacts
open. No bibliography, publication title, edition, theorem number, page,
quotation, or errata record is supplied.

Consequently this intake asserts no primary-source candidate. The phrase may
refer to a construction, symbolic-calculus formula, boundedness result, or
remainder estimate. Choosing among them would invent missing mathematics.

## Crosswalk

| Source element | Information fixed | Information still required for a theorem | Intake result |
|---|---|---|---|
| "paracomposition" | a paradifferential-calculus topic | exact operator definition and theorem family | unresolved |
| "复合函数" | composition is involved | types, domains, map hypotheses, local/global setting | unresolved |
| "仿微分" | paradifferentiation is involved | dyadic decomposition, quantization, regularity scale | unresolved |
| Jean-Michel Bony / 1981 | an unverified attribution and date | primary publication, exact theorem/page, errata | unresolved |
| `已验证` | repository screening label only | inspectable human proof or kernel receipt | no credit |

## Lean boundary and next gate

Repository search found no target-specific legacy Lean module or declaration.
No proposed Lean type is recorded because no unique source theorem has been
identified. The next gate must first locate and independently verify a primary
source, then produce a row-by-row mapping of every domain, binder, hypothesis,
conclusion, convention, and boundary case to a canonical Lean expression.
Only after that mapping may imports, universes, typeclasses, foundation/TCB
profiles, and mutation tests be frozen. Current debt is `formalization_debt`
provisionally; the existence and status of any external formal proof remain
unaudited and receive no credit.
