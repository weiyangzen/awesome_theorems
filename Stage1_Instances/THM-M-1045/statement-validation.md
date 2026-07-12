# Statement validation record

Item: `S56-M-1045-STATEMENT`  
Base revision: `003528e41c522d26270c91f61e92d738221c03c8`

## Frozen target

`Stage1Instances.THM_M_1045.CameronMartinTarget` freezes the Wiener-space statement on continuous
real paths over `NNReal`. Translation is the push-forward under `x |-> x + h`. A direction is
admissible precisely when it is the indefinite integral of an `L2` function. The target includes
mutual absolute continuity iff admissibility, the positive-sign exponential RN density, and mutual
singularity outside the Cameron-Martin space.

`WienerData` exposes the missing pinned-library construction boundary: Wiener-law premises and a
measurable Paley-Wiener pairing, but no quasi-invariance, density identity, or singularity result.
Thus the declaration is not the legacy circular model whose fields already assumed the conclusion.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment. No update,
build, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1045/Statement.lean` | 0 | target, direct expansion, four structural mutations, zero-direction boundary, and explicit expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-1045/check_statement.py` | 0 | expression SHA-256 `e1b35bb7a569b9a4279ea7eb729ccd5e45a62663fb645a68aeb03e41274c5cea`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-1045/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `13e17c...e93`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | rank 238, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/statement.json >/dev/null` | 0 | structured statement artifact is valid JSON |
| forbidden-term scan of `Statement.lean` and `check_statement.py` | 1 | no forbidden proof-device token found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-1045 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The expression validator distinguishes deletion of the singularity half, reversal to `x-h`,
weakening equivalence to one-way absolute continuity, and removal of the integral representation
linking the direction to its `L2` function. `zero_isCameronMartinDirection` checks the zero boundary.

This is self-tested statement evidence pending master acceptance. It does not prove Cameron-Martin,
accept human-source fidelity, construct Wiener measure, or advance any dependent execution node.
