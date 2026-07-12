# Statement validation record

Item: `S56-M-1078-STATEMENT`
Base revision: `a17f2bfe82ce19994b641db8436a12b449276a23`

## Frozen target

`Stage1Instances.THM_M_1078.MartingaleTransformTarget` freezes the finite-horizon discrete-time
qualitative transform inequality selected by intake. For every `p : ENNReal` with `1 < p < infinity`,
one nonnegative real constant works uniformly over every probability space, natural-number
filtration, real martingale, predictable real multiplier process bounded pointwise by one, and
horizon `n`. The transform is exactly
`sum k in range n, v (k+1) * (f (k+1) - f k)` and the conclusion compares its `lpNorm` with that
of `f n`. `MemLp (f n) p mu` is explicit.

The horizon-zero transform is the empty sum. Multipliers zero, one, and negative one are admitted.
The endpoints `p = 1` and `p = infinity` are excluded. The multiplier bound is deliberately
pointwise rather than almost-everywhere; transporting to an a.e. convention is downstream work.
`target_iff_expandedSourceShape` checks the direct expansion. Removed predictability, exponent two
only, and a circular assumed-bound formulation are separately elaborated mutations.

Minimal direct imports are `Mathlib.Probability.Martingale.Basic` and
`Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm`.

## Commands and results

All commands used the existing pinned environment and did not mutate `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1078/Statement.lean` | 0 | target, transform, expanded equivalence, and three mutations elaborated; explicit target printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1078/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `a5412e...a0e`, `651c8a...b1d2`, `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520; L0/rework-required; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no output |

## Status boundary

This is self-tested statement evidence pending master acceptance. It proves no martingale-transform
inequality and claims no `H0`, `M0`, audit completion, or theorem completion. Pinpoint primary-source
normalization and candidate theorem auditing remain downstream gates.
