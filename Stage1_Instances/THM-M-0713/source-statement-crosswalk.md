# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` supplies the name, attribution, year, and short gloss "the
negative solution of Hilbert's tenth problem". `Docs/Stage0_Blueprint.md` repeats it but explicitly
leaves the exact definitions and premises open. A separate computer-science record states the more
specific consequence "there is no algorithm deciding whether an arbitrary Diophantine equation has
an integer solution"; it is a distinct Stage0 UID and is not automatically the authority for this
target.

These records establish intake provenance, not a source-stable mathematical statement or H0.

## Candidate primary sources

Yuri Matiyasevich's 1970 work completing the Davis-Putnam-Robinson program is the historical primary
source family, but this intake has not pinned and independently inspected an immutable edition,
theorem number/pages, original hypotheses, translation, corrections, or errata. Martin Davis,
*Hilbert's Tenth Problem is Unsolvable* (American Mathematical Monthly 80 (1973), 233-269), is a
secondary proof source cited by mathlib and a useful crosswalk candidate, not H0 evidence here.

Mario Carneiro, *A Lean formalization of Matiyasevic's theorem* (2018), is the formalization source
cited by the pinned mathlib modules. Its exact source/revision and node mapping remain for the later
anchor audit.

## Crosswalk

| Repository/source phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Matiyasevich theorem" | commonly the final exponential-growth/Diophantine representation step | `Dioph`, `DiophFn`, Pell sequence machinery, and exponentiation graph | pinned APIs and anchors found; exact source correspondence unaudited |
| "negative solution" | nonexistence of a universal decision algorithm | explicit algorithm model plus an undecidability theorem | no exact repository definition or root declaration |
| "Hilbert's tenth problem" | integer-polynomial existential solvability | encoded finite multivariate integer polynomials and integer solutions | mathlib's local `Poly`/`Dioph` uses natural tuples and integer-valued polynomial functions; transport open |
| MRDP bridge | c.e. sets are Diophantine | computability definitions and a representation theorem | adjacent `THM-M-0714`; relationship must be frozen |
| `已验证` | untrusted inventory label | no proposition or kernel receipt | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.NumberTheory.PellMatiyasevic` contains `Pell.matiyasevic`, and
`Mathlib.NumberTheory.Dioph` contains `pell_dioph` and `pow_dioph`. Module documentation describes
`pow_dioph` as a version of Matiyasevich's theorem and explicitly lists "Finish the solution of
Hilbert's tenth problem" as TODO. Thus there is real partial machine evidence, but not evidence for
the broad repository gloss.

The bounded intake probe elaborates these public declarations. This is discovery evidence only,
not the dependency-ordered immutable anchor audit, terminal-body provenance audit, or root closure.
