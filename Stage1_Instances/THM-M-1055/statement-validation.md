# Statement validation record

Item: `S56-M-1055-STATEMENT`  
Base revision: `87a5a772b2a40a6b42b5951e3477471611d55d6c`

## Frozen target

`Stage1Instances.THM_M_1055.BirkhoffErgodicTarget` is the exact real-valued ergodic specialization
frozen by intake. It universally quantifies a measurable space and probability measure, an
ergodic self-map, and an integrable real observable. Its conclusion is almost-everywhere `atTop`
convergence of mathlib's first-`n` Birkhoff averages to the observable's integral.

Mathlib's `Ergodic T mu` includes measurability and measure preservation. Its `birkhoffAverage`
uses `Finset.range n`, hence the terms indexed `0` through `n - 1`, and defines the `n = 0` term as
zero. That single initial term does not change `atTop` convergence. Since `mu` is a probability
measure, the integral is the space mean without another normalization factor. No nonemptiness or
completeness assumption was silently introduced.

The three imports are source-level minimal: removing them one at a time makes elaboration fail at
`birkhoffAverage`, `Ergodic`, and the integral notation/API, respectively.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` environment.
No dependency or cache mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1055/Statement.lean` | 0 | target, definitional expanded-target iff, four mutations, and explicit target expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-1055/check_statement.py` | 0 | expression SHA-256 `8d7956f1...26181`; all four structural mutations distinguished |
| three deletion trials, each removing one direct import before `lake env lean` | 1 each | expected unknown `birkhoffAverage`, unknown `Ergodic`, and integral parse/API failures |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1055/Statement.lean lean-toolchain lake-manifest.json` | 0 | `a4caeaa6...2625`, `651c8acc...85b1d2`, `321626c8...b2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | recorded in final self-test run |
| `python3 scripts/stage1_target.py check` | 0 | recorded in final self-test run |
| `python3 scripts/stage1_target.py show THM-M-1055` | 0 | recorded in final self-test run |
| `python3 -m json.tool Stage1_Instances/THM-M-1055/statement.json` | 0 | recorded in final self-test run |
| forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no forbidden proof-gap declarations; `rg` uses 1 for no matches |
| `git diff --check -- Stage1_Instances/THM-M-1055 .stage1-worker-selftest.json` | 0 | recorded in final self-test run |

## Status boundary

The validator distinguishes removal of ergodicity, removal of integrability, a change from real to
complex observables, and replacement of the integral limit by zero. This is statement-only kernel
evidence pending master acceptance. Primary-source H0 review, anchor audit, proof, hermetic replay,
and independent acceptance remain downstream and no theorem completion is claimed.
