# Statement validation record

Item: `S56-M-1522-STATEMENT`  
Base revision: `bc7ff7c864291d915984b6d9312ed0ea7d160161`

## Frozen target

`Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget` is the exact intake-selected
ergodic probability-space specialization for real-valued integrable observables. `Ergodic T mu`
includes measurability and measure preservation. The conclusion retains the mandatory
almost-everywhere qualifier and uses mathlib's `birkhoffAverage Real T f` with limit
`MeasureTheory.integral mu f`.

The three direct imports are minimal for this source: deleting them individually rejects the
Birkhoff-average, ergodicity, or Bochner-integral vocabulary. The legacy Hilbert mean-ergodic
module is not imported. `birkhoffTarget_iff_expandedFiniteSumTarget` kernel-checks the direct
finite-orbit-sum encoding without invoking a convergence theorem.

## Commands and results

All Lean commands ran from `Formalizations/Lean` with the existing pinned toolchain and canonical
`.lake` artifacts. No dependency update, fetch, clone, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1522/Statement.lean` | 0 | exact target, direct-sum iff, and four structural mutations elaborated; explicit target expression printed |
| `python3 Stage1_Instances/THM-M-1522/check_statement.py` | 0 | expression SHA-256 `1ae3d8a352060fb26372a07d0128af2f465933e4c3c08b6c752b0b5fe72c83b5`; all four mutations distinguished |
| delete each direct import separately in a temporary copy and run `lake env lean` | 1 each, expected | each removal produced unknown identifiers belonging to that import's statement vocabulary |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1522/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `2ef66f...d87c`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-1522` | 0 | rank 190, planned lifecycle, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects replacing ergodicity with mere
measure preservation, removing integrability, removing probability normalization, or strengthening
almost-everywhere convergence to convergence at every point. `n = 0` remains in the sequence and
has average zero by mathlib's definition, harmless for an `atTop` limit. The target adds neither
invertibility of `T` nor a nonempty-space premise.

This is statement-only evidence pending master acceptance. It supplies no Birkhoff proof and does
not advance anchor-audit, obligation-tree, proof, validation, or release nodes.
