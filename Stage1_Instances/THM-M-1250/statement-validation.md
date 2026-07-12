# Statement validation record

Item: `S56-M-1250-STATEMENT`  
Base revision: `c370639c4481be6bdcec40b9aa3553046d6f7572`

## Frozen target

`Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization` fixes the intake's canonical scope:
complex-valued functions on `R^n`, represented as `Fin n -> Real`, including `n = 0`. Membership is
function-level existence of a bundled mathlib `SchwartzMap`. Its right side explicitly requires
infinite differentiability and a uniform bound for every polynomial weight and every iterated
Frechet-derivative order. The sole direct import is
`Mathlib.Analysis.Distribution.SchwartzSpace.Basic`.

The theorem `exists_representative_iff_nonempty` checks transport to the equivalent subtype
encoding. The structural validator distinguishes mutations of codomain, smoothness, derivative
orders, and the zero-dimensional boundary.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment. No update,
build, fetch, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1250/Statement.lean` | 0 | canonical target, checked transport, and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1250/check_statement.py` | 0 | expression SHA-256 `367a6b23168c88dcc5023a4d82bff17b496187a25303b4f81871a321750205f0`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1250/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `bb3cc8...e39f`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` (repository root) | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` (repository root) | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` (repository root) | 0 | rank 430, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

An initial invocation of the last three repository scripts from `Formalizations/Lean` exited 2
because their repository-relative paths do not exist from that directory. They were rerun from the
repository root as recorded above; this operator-path error did not affect Lean elaboration.

This is statement-only evidence pending master acceptance. It does not prove the characterization
or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
