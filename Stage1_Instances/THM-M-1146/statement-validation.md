# Statement validation record

Item: `S56-M-1146-STATEMENT`  
Base revision: `3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`

## Frozen target

`Stage1Instances.THM_M_1146.SchwarzReflectionTarget` elaborates the intake-selected harmonic,
zero-boundary form of the Schwarz reflection principle. Its domain is an open, conjugation-invariant
set `V`. The input is harmonic on the strict upper part, continuous through the real-axis portion,
and zero there. Its explicitly defined odd reflection must be harmonic on all of `V` and agree with
the input above the axis.

The two direct imports are the module defining `HarmonicOnNhd` and the module supplying the
`FiniteDimensional Real Complex` instance it requires. No holomorphic reflection theorem or proof
module is imported.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` artifacts. No
update, fetch, clone, or broad build command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1146/Statement.lean` | 0 | target, five mutations, two branch-boundary lemmas, and explicit target print elaborated |
| `python3 ../../Stage1_Instances/THM-M-1146/check_statement.py` | 0 | expression SHA-256 `14336b88fd9aa11228ee9c7a86cc56a3473702bc2f8d77e266f2b4d37deef53d`; all five mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-1146/Statement.lean lean-toolchain lake-manifest.json` | 0 | statement `1eed153...f5dd`, toolchain `651c8a...1d2`, manifest `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | rank 351, planned, L0/rework-required, theorem incomplete |

The structural checker distinguishes removal of openness, symmetry, continuity, or zero boundary
values, and replacement of odd by even reflection. Kernel-checked branch lemmas fix the axis and
lower-half-plane conventions. These checks freeze syntax and scope; they do not prove the theorem.

Statement elaboration is self-tested pending master acceptance. Anchor audit, proof, release gates,
and theorem completion remain open.
