# Statement validation

Item: `S56-M-1023-STATEMENT`

## Frozen target

`Stage1Instances.THM_M_1023.InfinitelyDivisibleIffLevyKhintchine` freezes the real-line
Levy-Khinchin characterization. Infinite divisibility explicitly requires `mu` and every
positive-order convolution root to be probability measures. Convolution power is recursive with
zeroth power `dirac 0`, while the definition quantifies only over `0 < n`.

The representation uses mathlib's positive-sign characteristic function and the truncation
`x * 1_{|x| <= 1}`. Data consist of a real drift, nonnegative Gaussian variance, and a jump measure
with no atom at zero and finite integral of `min 1 x^2`. The representation data are required to be
unique in this fixed convention. Zero drift, zero Gaussian variance, and the zero jump measure are
not excluded.

The sole direct import is `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`. It exposes
`charFun`, measure integration, probability measures, and additive convolution in the pinned
mathlib snapshot. `target_iff_expanded` kernel-checks a direct expansion of the selected target.

## Commands and results

Commands ran on 2026-07-12 from `Formalizations/Lean` using the existing pinned `.lake` artifacts.
No dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1023/Statement.lean` | 0 | target, direct expansion, checked transport, and five structural mutations elaborated |
| `python3 Stage1_Instances/THM-M-1023/check_statement.py` | 0 | expression SHA-256 `f84253...e1a2f`; all five mutations distinguished; statement file SHA-256 `ebb29f...e296` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1023/Statement.lean lean-toolchain lake-manifest.json` | 0 | `ebb29f...e296`, `651c8a...b1d2`, `321626...5cb2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1023` | 0 | rank 499; planned; theorem completion false |

Environment pins: repository base `aaeade67ccb391b2d10e50e766d54427324b3090`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` from `lakefile.lean` and the pinned manifest.

## Mutation and status boundary

The separately elaborated mutations remove the probability hypothesis on `mu`, admit convolution
order zero, change the measure domain to `Complex`, drop the converse, and exclude a zero Gaussian
component. They are intentionally not asserted equivalent to the canonical target.

This is self-tested statement elaboration pending master acceptance. The statement phase selects a
standard normalization, but source-edition pinpointing and independent convention review remain
the dependent anchor-audit task. No proof, `H0`, audit completion, or theorem completion is claimed.
