# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives only the Chinese title "激波理论", attribution to many
mathematicians, twentieth century, the wording "守恒律方程的激波", importance "high", and the
untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields while leaving definitions,
hypotheses, proof history, axioms, machine status, and artifact links open. No bibliography,
edition, theorem number, page, definitions, or errata record is attached.

Therefore no primary-source candidate or exact theorem is asserted at intake. Shock wave theory
contains many inequivalent theorems; choosing one now would substitute new mathematics for the
source record. The metadata label receives no `H0` or machine-proof credit.

## Crosswalk

| Source element | Information genuinely fixed | Information required for Lean | Intake result |
|---|---|---|---|
| "conservation-law equations" | some conservation law is involved | equation, dimensions, state space, flux and regularity | unresolved |
| "shock waves" | discontinuous-wave behavior is intended | weak solution, discontinuity geometry and traces | unresolved |
| "theory" | a family of results, not a proposition | exact quantified conclusion | unresolved |
| twentieth century / many mathematicians | broad history | primary edition, theorem/page and errata | unresolved |
| `已验证` | secondary metadata | inspectable human proof or kernel receipt | no credit |

## Statement boundary and first gate

No canonical Lean declaration or expression exists at intake, and no alternate encoding can yet be
checked. The first downstream gate is identification of one primary theorem whose scope legitimately
matches the repository label. Before `H0`, independent review must verify the edition, theorem/page,
definitions, every assumption, conclusion, and errata, then approve a row-by-row source-to-Lean
crosswalk. The adjacent Rankine-Hugoniot record may become a dependency only after that selection;
it is not the root claim by default.
