# S56-M-0400-STATEMENT validation

## Frozen target

`Stage1Rev56.THMM0400.Statement` is the exact Lean proposition selected from
the intake's archimedean product-of-linear-forms scope. It fixes dimension
`n >= 2`, algebraic complex coefficients, complex-linear independence,
positive epsilon, supremum height on integer vectors, a strict `Real.rpow`
product inequality, and containment in a finite family of proper rational
submodules.

The repository and intake do not provide a verified primary-source theorem
number/page. Consequently this artifact establishes exact elaboration of the
selected scope, not H0 source fidelity. The downstream anchor audit must
pinpoint the source and either confirm this normalization or supply a checked
transport. No proof body, audit completion, or theorem completion is claimed.

## Commands and results

Base revision: `37bf5277bf057d41d0711172bc2cd11f43b2a0ce`.

- `python3 Docs/tools/check_stage1_standard.py`: exit 0; 15 assurance groups,
  41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed.
- `python3 scripts/stage1_target.py check`: exit 0; 1546 unique targets with
  ranks 1 through 1546 passed.
- `python3 scripts/stage1_target.py show THM-M-0400`: exit 0; rank 13, L0,
  rework required, planned, theorem incomplete.
- From `Formalizations/Lean`, `lake env lean --version`: exit 0; Lean 4.29.0,
  commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- From `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-0400/Statement.lean`:
  exit 0; output `Stage1Rev56.THMM0400.Statement : Prop`.
- `python3 -m json.tool Stage1_Instances/THM-M-0400/statement.json`: exit 0.
- `git diff --check -- Stage1_Instances/THM-M-0400`: exit 0.

The existing untracked `Formalizations/Lean/.lake` link is outside the owned
path and was not modified intentionally. This is worker self-test evidence,
not hermetic release evidence or master acceptance.
