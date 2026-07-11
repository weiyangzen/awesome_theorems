# Source-statement crosswalk

## Repository source

The repository-local research record (`Docs/researches/math_theorems.md`) says only:
"fully nonlinear elliptic equations," twentieth century, attributed to many mathematicians, with
the statement "Monge-Ampere equations, etc." `Docs/Stage0_Blueprint.md` repeats this metadata and
adds no definition, hypotheses, conclusion, or primary citation. The generated status `已验证` is
not evidence under rev-5.6.

No primary mathematical source is cited by the input. Consequently this intake does not nominate a
source theorem from memory. Edition/article, theorem number, page, exact assumptions, dependencies,
and errata all remain open, so the human-source state is `H4` rather than `H0`.

## Crosswalk

| Input fragment | Missing mathematical choice | Required Lean surface | Status |
|---|---|---|---|
| "fully nonlinear" | exact nonlinear operator and dependence on `x,u,Du,D2u` | typed operator on jets/Hessians | open |
| "elliptic" | degenerate/uniform ellipticity and matrix-order convention | symmetric matrices, Loewner order, constants | open |
| "equations" | domain, boundary conditions, and equality/inequality | sets, boundary traces, equation predicate | open |
| "Monge-Ampere" | classical determinant or weak measure formulation | Hessian determinant or Monge-Ampere measure | example only |
| "etc." | which other family, if any | none can be encoded faithfully | inadmissibly vague |
| theorem conclusion | comparison/existence/uniqueness/estimate/regularity | one exact `Prop` with quantified constants | absent |
| solution | classical/viscosity/Alexandrov and regularity | explicit solution predicate | absent |

## Existing formal-artifact boundary

Repository search found legacy Monge-Ampere-oriented modules `S1_M_148.lean` through
`S1_M_150.lean`, but those belong to other historical targets and explicitly describe missing PDE
infrastructure. They are discovery inputs only and are neither an exact anchor nor proof credit for
THM-M-1178. The later anchor-audit phase must search the pinned mathlib revision and credible Lean 4
projects after the exact source statement is frozen.

Before `H0`, an independent reviewer must approve a primary-source pinpoint and a row-by-row mapping
of definitions, ordered binders, every hypothesis, conclusion, exceptional cases, dependencies, and
errata to the canonical Lean target.
