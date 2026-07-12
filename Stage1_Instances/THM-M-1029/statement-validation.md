# Statement validation record

Item: `S56-M-1029-STATEMENT`  
Base revision: `2f58f2b8e57dc8637559b8e90ecc72cc391f498a`

## Frozen target

`Stage1Instances.THM_M_1029.LevyMartingaleCharacterizationTarget` formalizes the intake claim over
`NNReal` time. The probability measure, filtration, pathwise continuity, almost-everywhere zero
start, and both martingale hypotheses are explicit. The conclusion says each increment after `s`
is independent of the filtration sigma algebra at `s` and has `gaussianReal 0 (t - s)` law.

The only direct imports are `Mathlib.Probability.Distributions.Gaussian.Real` and
`Mathlib.Probability.Martingale.Basic`. `target_iff_expandedSourceShape` kernel-checks the direct
expansion. This freezes a non-circular Brownian conclusion rather than the legacy abstract package.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1029/Statement.lean` | 0 | target, direct expansion, four mutations, and zero-elapsed boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1029/check_statement.py` | 0 | expression SHA-256 `f3e443377f8cac2eba62a6ebcf6f05ce5bd453f3075d9de573641856e21331b2`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1029/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `ae6a30...782`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, uniform L0/rework-required |
| `python3 -m json.tool Stage1_Instances/THM-M-1029/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1029` | 0 | no whitespace errors |

## Mutation and status boundary

The validator compares explicit elaborated expressions and distinguishes removing the quadratic
martingale hypothesis, changing the time domain to `Nat`, existentially rebinding the filtration,
and excluding the `s = t` boundary. The boundary theorem checks `t - t = 0` in `NNReal`.

This is self-tested statement evidence pending master acceptance. The exact primary-source pinpoint
and independent source-convention review remain for anchor audit, so no `H0`, proof, audit
completion, or theorem completion is claimed.
