# S56-M-0397-STATEMENT validation

Base revision: `cc9d29a4da006a94c9896124b7ef9fe253befac3`.

The canonical target is `Stage1Rev56.THMM0397.Statement`. It elaborates from
two direct pinned imports. It expresses the exact method-level reading of the
catalogue claim: a supplied Baker lower bound and a supplied problem-specific
reduction yield an executable exhaustive solution list. It neither proves
those premises nor selects an unmentioned Diophantine equation.

## Commands and results

| Command | Cwd | Exit | Result |
|---|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | repository root | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | repository root | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0397` | repository root | 0 | rank 10, planned, L0/rework_required, theorem incomplete |
| `lake env lean --version` | `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lean ../../Stage1_Instances/THM-M-0397/Statement.lean` | `Formalizations/Lean` | 0 | `Stage1Rev56.THMM0397.Statement.{u} : Prop` |
| remove `Mathlib.Analysis.SpecialFunctions.Complex.Log` in a `/tmp` copy, then run `lake env lean` | `Formalizations/Lean` | 1 | complex algebra, norm, and exponential substrate unavailable |
| remove `Mathlib.FieldTheory.AlgebraicClosure` in a `/tmp` copy, then run `lake env lean` | `Formalizations/Lean` | 1 | `IsAlgebraic` unavailable |

The statement source SHA-256 is
`78327c7641064bddbf5acb119253a5956e27c78a5c69b3fc04de7563b055c07f`.
The pre-existing untracked `.lake` symlink resolves to the canonical pinned
cache; its mathlib checkout is exactly
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and was not modified. No update,
fetch, clone, or broad build was run. This is narrow statement elaboration
evidence, not proof, hermetic release evidence, or master acceptance.
