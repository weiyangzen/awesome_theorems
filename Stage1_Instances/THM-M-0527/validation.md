# Intake validation

Base revision: `33db6c6fe92d3a3ab683d2fbc8ab03cd68505e8e`. Commands ran from the worker
clone on 2026-07-12. The Lean command ran against the existing canonical `.lake` symlink; no update,
fetch, build, or dependency mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | rank 584; planned; `hard_statement_first_partial_verification`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0527/intake.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0527/task-dag.json >/dev/null` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0527/IntakeSmoke.lean)` | 0 | elaborated `IsCoveringMap`, `FundamentalGroup`, `IsCoveringMap.monodromyFunctor`, and `IsCoveringMap.existsUnique_continuousMap_lifts` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2`; `321626c8...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-0527` | 0 | no whitespace errors |

This is node-scoped intake evidence only. The exact classification expression, source acceptance,
obligation registry, proof, and release gates remain open. The pre-existing untracked
`Formalizations/Lean/.lake` symlink is canonical automation infrastructure and was not modified;
the run is nonrelease evidence in any event.
