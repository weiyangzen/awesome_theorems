# Statement validation record

Item: `S56-M-0994-STATEMENT`  
Base revision: `8d7cfb9e267efd34427f29cb4d7103282a0d0942`

## Frozen target

`Stage1Instances.THM_M_0994.HoeffdingTarget` freezes the one-sided centered upper-tail inequality
for an arbitrary finite family. The binders retain a probability measure, coordinate
measurability, independence, almost-sure interval bounds, and a nonnegative threshold. Its
conclusion uses the exact classical exponent `(-2 * epsilon^2) / sum_i (b_i-a_i)^2`.

The empty family, threshold zero, and zero total width are included. Lean's real division defines
division by zero as zero, so the displayed exponential is `exp 0 = 1` when the denominator is zero.
This is an explicit encoding boundary rather than a hidden positive-denominator assumption.

## Minimal imports

The statement elaborates using only `Mathlib.Probability.Independence.Basic`,
`Mathlib.MeasureTheory.Integral.Bochner.Basic`, and `Mathlib.Analysis.SpecialFunctions.Exp` from
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The legacy SubGaussian module is not imported.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0994/Statement.lean` | 0 | exact target and four structural mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0994/check_statement.py` | 0 | expression SHA-256 `b8667e40b1500ad131f407ebdc2eb5d810de5593310c3a57d16178da79545409`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0994/Statement.lean lean-toolchain lake-manifest.json` | 0 | `55d06a...e7e9`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0994` | 0 | rank 274, planned, L0/rework-required, theorem incomplete |

The mutation validator distinguishes removal of independence, specialization of the finite index
domain, altered measurability binder scope, and exclusion of the zero-width boundary. This receipt
is statement-only evidence pending master acceptance. It does not credit the historical wrapper,
prove Hoeffding's inequality, or advance any dependent node.
