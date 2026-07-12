# Statement validation record

Item: `S56-M-1024-STATEMENT`  
Base revision: `aaeade67ccb391b2d10e50e766d54427324b3090`

## Frozen target

`Stage1Instances.THM_M_1024.LevyKhintchineTarget` elaborates the intake-selected finite-dimensional
probability-law equivalence. The statement locally defines probability convolution powers,
infinite divisibility, Levy triplets, the symmetric positive-semidefinite covariance conditions,
the Levy-measure conditions, and the characteristic exponent. Its sole direct import is
`Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`.

The convention is `+i`, Gaussian coefficient `-1/2`, and compensation on `norm x <= 1`.
Representation data are under `ExistsUnique`, so uniqueness is not silently discarded. Dimension
zero, zero covariance, and zero jump measure are not excluded. The separately elaborated mutations
remove uniqueness, specialize the dimension, remove the zero-atom condition, and change the closed
unit ball to an open ball.

## Commands and results

All commands ran in this worker clone; the Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1024/Statement.lean` | 0 | Exact target, definitions, four structural mutations, and dimension-zero boundary probe elaborated; explicit target expression printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-1024/Statement.lean lean-toolchain lake-manifest.json` | 0 | `197a719...a87`, `651c8ac...1d2`, `321626c...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1024` | 0 | rank 500, planned, L0/rework-required, theorem incomplete |

This is statement-only evidence pending master acceptance. It does not prove the theorem or advance
the anchor-audit, obligation-tree, proof, validation, or release nodes.
