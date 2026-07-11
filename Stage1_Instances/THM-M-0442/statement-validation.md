# Statement validation record

Item: `S56-M-0442-STATEMENT`  
Base revision: `bfbe742ac9af5c19d967a13446453e097e5f9241`

## Frozen target

`Stage1Instances.THMM0442.MazurRationalTorsionTarget` is the intake-selected necessity direction:
for every elliptic Weierstrass curve over `Rat`, its rational torsion group is one of the cyclic
types of orders 1 through 10 or 12, or `ZMod 2 x ZMod (2*m)` for `1 <= m <= 4`. It does not add the
realizability converse. Its only direct imports are the affine rational-point module and the
additive torsion API.

`HistoricalCandidateShape` restates the historical `{2,4,6,8}` second-factor encoding.
`legacy_second_order_iff` checks the reindexing, and
`mazurRationalTorsionTarget_iff_historicalCandidateShape` checks the full statement transport.

## Commands and results

Lean commands ran from `Formalizations/Lean` through the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0442/Statement.lean` | 0 | canonical target, historical transport, four mutations, and endpoint boundaries elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0442/check_statement.py` | 0 | expression SHA-256 `b65a3a...1658`; all four mutations distinguished; pinned mathlib revision reported |
| import deletion tests using `sed` into temporary Lean files, followed by `lake env lean` | 1 for each retained import | deleting `Affine.Point` or `GroupTheory.Torsion` breaks elaboration; deleting `Data.ZMod.Basic` succeeded, so that redundant import was removed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0442/Statement.lean lean-toolchain lake-manifest.json` | 0 | `8779e8...5ce4`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | rank 88; planned; historical artifacts unaccepted; theorem incomplete |

The validator distinguishes omission of order 12, admission of index zero, changing the universal
curve binder to an existential, and adding realizability. Kernel-checked boundary theorems exercise
cyclic orders 1, 10, and 12 and noncyclic indices 1 and 4. This is statement-only evidence pending
master acceptance; it supplies no proof of Mazur's theorem and no later-node evidence.
