# Statement validation record

Item: `S56-M-1527-STATEMENT`  
Base revision: `4161921b2a43484a498bcf39900c1c468bc4174e`

## Frozen target

`Stage1Instances.THM_M_1527.MaxwellCoordinateEquivalence` formalizes the exact theorem family
selected at intake: after positive SI constants and a convention-dependent coordinate
decomposition are supplied, the four classical equations are equivalent to `dF = 0` and
`d(star F) = J`. The Hodge star and the two component-decomposition equivalences are explicit
model data. Thus the statement does not pretend mathlib already constructs Lorentzian geometry,
and it does not weaken the target to projections from an assumed Maxwell solution.

The sole direct import is `Mathlib.Analysis.Calculus.DifferentialForm.Basic`. The statement fixes
classical space to `Fin 3 -> Real`, while leaving the covariant normed spacetime universe explicit
and recording dimension four, mostly-plus Lorentzian signature, and spacetime/time orientation as
checked hypotheses. Zero fields and zero current are admitted; nonpositive vacuum constants are excluded.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` and reused the
existing pinned `.lake`; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1527/Statement.lean` | 0 | canonical target and all four structural mutations elaborated; explicit expressions printed |
| `python3 ../../Stage1_Instances/THM-M-1527/check_statement.py` | 0 | canonical SHA-256 `b1bbba...adc9`; removed-hypothesis, changed-domain, changed-scope, and one-way mutations all differed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1527/Statement.lean lean-toolchain lake-manifest.json` | 0 | `9520e4...2658`, `651c8a...b1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1527` | 0 | rank 195, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1527/statement.json >/dev/null` | 0 | statement certificate is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1527 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test receipt creation |

This is statement-only evidence pending master acceptance. It gives no proof credit and does not
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
