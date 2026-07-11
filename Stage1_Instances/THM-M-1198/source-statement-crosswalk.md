# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "method of characteristics", attribution
to multiple mathematicians, eighteenth century, the phrase "a method for solving first-order
hyperbolic equations", importance "high", and the untrusted label `已验证`.
`Docs/Stage0_Blueprint.md` lists the title without a bibliography. No author, edition, theorem
number, page, hypotheses, proof, or errata record is attached.

Consequently no primary-source candidate is asserted at intake. The phrase covers inequivalent
linear transport representation theorems, quasilinear local existence results, Hamilton-Jacobi
constructions, and characteristic initial-value problems. Selecting one now would substitute
missing mathematics, so the source label receives no `H0` credit.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "first-order" | highest derivative order is one | precise derivative and function-space API | unresolved |
| "hyperbolic equations" | broad PDE class | actual operator and hyperbolicity assumptions | unresolved |
| "characteristics" | auxiliary curves should encode the PDE | characteristic ODE, flow, chain rule, interval | unresolved |
| "solving" | some solution construction is intended | existence, uniqueness, formula, and solution predicate | unresolved |
| eighteenth century / multiple authors | broad historical attribution | none | insufficient to identify a theorem |
| `已验证` | untrusted repository label | inspectable source proof and kernel receipt | no credit |

## First downstream gate

The statement phase must first identify a primary source whose theorem makes one exact claim. An
independent reviewer must verify its edition, page, assumptions, definitions, conclusion, and
errata, then approve a row-by-row mapping to a canonical Lean expression. Until then there is no
eligible Lean target and no anchor can receive proof credit.
