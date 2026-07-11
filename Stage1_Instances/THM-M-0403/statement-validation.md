# Statement validation record

Item: `S56-M-0403-STATEMENT`  
Base revision: `cdc74d2233a90bfe43066d639abb923202621260`

## Frozen target

The canonical declaration is
`Stage1.THM_M_0403.SchlickeweiEvertseStatement`. It quantifies over a
characteristic-zero field, a positive number of terms, and data carrying
nonzero coefficients, nonzero roots, and nontorsion quotients for every pair
of distinct roots. Its conclusion is finiteness of the natural-number zero
set. The exact-type fixture in `Statement.lean` checks the ordered target
surface by definitional equality.

The direct imports are only `Mathlib.Algebra.Field.Basic` (field and finite-sum
surface) and `Mathlib.GroupTheory.OrderOfElement` (`IsOfFinOrder`). The legacy
module's height, number-field, recurrence, S-integer, and roots-of-unity imports
are not needed to elaborate this statement.

## Commands and results

All commands ran in this worker clone. The Lean command ran from
`Formalizations/Lean` so it reused the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0403/Statement.lean` | 0 | no output; canonical declaration and exact-type fixture elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0403` | 0 | rank 16, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0403/statement.json >/dev/null` | 0 | statement receipt is valid JSON |
| `sha256sum Stage1_Instances/THM-M-0403/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match `statement.json` |
| `git diff --check -- Stage1_Instances/THM-M-0403 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary and mutations

The target is deliberately not broadened to repeated-root recurrences or the
Skolem--Mahler--Lech periodic conclusion. Removing positivity permits the empty
sum, removing either nonzero field permits collapsed terms, removing pairwise
nontorsion admits periodic cancellation, and changing `Nat` changes the zero
index domain. Those are statement changes rather than accepted transports.
No alternate encoding is credited by this node.

This receipt establishes statement elaboration only. It contains no proof of
the root proposition and does not advance theorem completion.
