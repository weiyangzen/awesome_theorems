# Statement validation record

Item: `S56-M-1550-STATEMENT`  
Base revision: `535a525f487a46804fc0abc236b3e993110c3c9d`

## Frozen target

`Stage1Instances.THM_M_1550.LaxPairIsospectrality` is the exact conservative claim selected at
intake. For arbitrary finite complex matrices on a real time domain, it retains both the matrix
Lax equation and an explicitly supplied conjugating evolution, and concludes equality of mathlib's
algebra spectrum at every two domain times. It does not assert that every integrable system admits
a Lax pair or that the conjugating evolution has already been constructed from the ODE.

The direct imports are `Mathlib.Analysis.Matrix.Normed` and
`Mathlib.Analysis.Calculus.Deriv.Basic`. The checked theorem
`laxPairIsospectrality_iff_pinnedCandidateSourceShape` verifies the direct predicate expansion.

## Commands and results

Commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean`, reused the
canonical pinned `.lake`, and performed no update, fetch, clone, or build.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1550/Statement.lean` | 0 | canonical target, checked direct expansion, four mutations, and empty/zero-dimensional boundary cases elaborated; explicit expressions printed |
| `python3 ../../Stage1_Instances/THM-M-1550/check_statement.py` | 0 | canonical SHA-256 `657174...194c`; removed-hypothesis, changed-domain, changed-scope, and changed-boundary mutations all differed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1550/Statement.lean lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-1550/check_statement.py` | 0 | `232e1c...952c`, `651c8a...b1d2`, `321626...d81`, `059aaf...9c3` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository rev-5.6 standard check passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1550` | 0 | rank 209, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |

This is statement-only evidence pending master acceptance. It gives no proof credit and does not
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
