# Source-statement crosswalk

## Candidate primary sources

- Laurent Schwartz, *Theorie des distributions*, Hermann, first edition volumes (1950-1951).
  This is the historical primary-source candidate; exact volume, edition, theorem/page, wording,
  assumptions, and errata have not yet been inspected.
- Lars Hormander, *The Analysis of Linear Partial Differential Operators I*, Springer. Its chapter
  on distributions is a modern authoritative candidate, but edition and exact definition/theorem
  anchor remain open.

These are discovery anchors, not `H0` evidence. The statement gate selects the exact interpretation
already documented by the pinned mathlib module: equality with the complex continuous dual carrying
pointwise convergence. A stable primary-source inspection is still required to determine whether a
stronger historical topology was intended; no such stronger claim is credited here.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "tempered distributions" | continuous functionals on rapidly decreasing tests | `TemperedDistribution E k` or exact replacement | included; parameters open |
| "Schwartz space" | smooth functions with all polynomially weighted derivatives bounded | `SchwartzMap E k` | included; source convention open |
| "dual" | continuous linear dual, possibly with specified topology | `PointwiseConvergenceCLM` over `SchwartzMap` | pointwise topology selected; source-strength audit open |
| base domain | usually `R^n` | arbitrary finite-dimensional real normed space | selected; includes dimension zero |
| scalars | real or complex distributions | complex-valued tests and functionals | complex convention selected |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_171.lean` imports
`Mathlib.Analysis.Distribution.TemperedDistribution` and records useful names, but rev-5.6 declares
all legacy artifacts unaccepted. Its normalized statement is described as a definitional
pointwise-convergence continuous dual, while it separately records the strong-dual interpretation
as unresolved. This distinction must be checked against the selected source before elaboration.

`Stage1_Instances/THM-M-1251/Statement.lean` elaborates the selected expression and checks its
direct expansion. Before `H0`, an independent reviewer must verify edition, exact page/theorem or
definition, all hypotheses, topology and scalar conventions, translations, and errata, and approve
every crosswalk row. Statement elaboration alone is neither `H0` nor `M0` proof evidence.
