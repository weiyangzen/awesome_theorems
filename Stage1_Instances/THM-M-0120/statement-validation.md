# Statement validation record

Item: `S56-M-0120-STATEMENT`  
Base revision: `bca606e3b3f7a0638b9d257751458c87a1ee5368`

## Frozen target

`Stage1Instances.THMM0120.MoriConeTheoremTarget` is the relative characteristic-zero klt-pair
package chosen at intake. It contains the cone decomposition as a finite-support Minkowski sum,
negative extremal rays, rational generators with the `2 * relativeDimension` length bound, local
finiteness uniformly away from the nonnegative wall, and the universal contraction of every ray.

The pinned mathlib revision has no native klt-pair or numerical-curve-class API. `ConeTheoremData`
therefore exposes those typed primitives but keeps every conclusion outside the data structure.
This avoids the legacy artifact's opaque output `Prop` fields. The exact source edition and theorem
number remain an H-gate obligation; this statement node freezes the intake choice rather than
claiming source-audit acceptance.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned `.lake` symlink; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0120/Statement.lean` | 0 | target, definitional expansion, and three mutations elaborated; explicit target expression printed with no warnings |
| `python3 ../../Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...88cfd`; removed-klt, absolute-base, and no-contractions mutations all distinguished; forbidden source tokens rejected |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0120/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `69eabc83...fd6b`, `651c8acc...1d2`, and `321626c8...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

This is statement-only evidence pending master acceptance. It supplies no theorem proof, anchor
credit, accepted task state, or completion claim.
