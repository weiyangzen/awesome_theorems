# Statement validation record

Item: `S56-M-1053-STATEMENT`  
Base revision: `87a5a772b2a40a6b42b5951e3477471611d55d6c`

## Frozen target

`Stage1.THM_M_1053.StatementShape` is the intake-selected real-valued Birkhoff pointwise ergodic
theorem. It explicitly binds a probability measure, a measure-preserving endomorphism, and an
integrable observable. Its witness is integrable and invariant almost everywhere; the forward
Cesaro averages converge to it pointwise almost everywhere. Ergodicity is used only to identify the
limit with the constant space integral.

The imports are `Mathlib.Dynamics.Ergodic.Function` and
`Mathlib.MeasureTheory.Integral.Bochner.Basic`. Removing the second import fails at the integral
notation, so both are required by this source. `timeAverage` assigns zero at `n = 0`, checked by
`timeAverage_zero`; this value cannot affect convergence along `atTop`.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1053/Statement.lean` | 0 | canonical target, four mutations, and zero-index boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1053/check_statement.py` | 0 | expression SHA-256 `f4b06a49160cd083fa4cf1bb3b1ddfe1453dbcb1e521ff2c09ba5d3753a2e562`; four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1053` | 0 | rank 245, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1053/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1053` | 0 | no whitespace errors |

The mutations remove the ergodic specialization, weaken probability to finite measure, assume the
desired convergence, and replace pointwise almost-everywhere convergence by integrated mean
convergence. None has the canonical elaborated expression. This is statement-only evidence pending
master acceptance; source review, proof, downstream validation, and theorem completion remain open.
