# Statement validation record

Item: `S56-M-0347-STATEMENT`  
Base revision: `c9694802ae049af37973e49a65f11b833135333f`

## Frozen target

`Stage1Instances.THM_M_0347.FejerTheoremTarget` quantifies over every positive real period and every
continuous complex-valued map on `AddCircle T`. Its symmetric partial sum contains precisely the
integer frequencies `-n, ..., n`; its `n`th Fejer mean averages `S_0, ..., S_n` with denominator
`n + 1`; its conclusion is convergence in the continuous-map topology, hence the intended uniform
convergence on the compact circle. The sole direct import is
`Mathlib.Analysis.Fourier.AddCircle`.

`fejerTheoremTarget_iff_expanded` kernel-checks the direct finite-sum expansion. This statement gate
does not prove Fejer's theorem or claim a primary-source pinpoint. That source debt remains `H1` and
must be handled by later audit work.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
pre-existing pinned `.lake` artifacts; no update, fetch, clone, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0347/Statement.lean` | 0 | exact target, direct expansion iff, four mutations, and two index-zero boundary lemmas elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0347/check_statement.py` | 0 | expression SHA-256 `ae3d7a520ec1089f6b6a798ee280d598bb18738b4eecf0042a8d9e7fbd3fa564`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-0347/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `040fee...c889`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0347` | 0 | rank 840, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The checker compares explicit elaborated expressions and distinguishes period specialization,
pointwise weakening, changed function-binder scope, and omission of the initial partial sum. The
kernel-checked boundary lemmas show that `S_0` contains exactly frequency zero and that the zeroth
Fejer mean equals `S_0`. Nonpositive periods are excluded; constant and zero functions are not.

This is statement-only evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, or release nodes, and `theorem_complete` remains false.
