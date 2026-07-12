# Statement validation record

Item: `S56-M-0708-STATEMENT`  
Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

## Frozen target

`Stage1Instances.THM_M_0708.RiceTheoremTarget` is the exact intake-selected functional form of
Rice's theorem. It quantifies over a semantic set of unary partial functions and requires positive
and negative witnesses that are each `Nat.Partrec`. It concludes that membership after
`Nat.Partrec.Code.eval` is not `ComputablePred`. Its sole direct import is
`Mathlib.Computability.Halting`.

The checked iff with `IntakePredicateShape` verifies the set/predicate presentation change.
Language and recursively enumerable-set presentations still require separate transports.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment. No Lake
dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0708/Statement.lean` | 0 | exact target, checked intake transport, four mutations, and empty/universal boundary lemmas elaborated; explicit target expression printed |
| `python3 Stage1_Instances/THM-M-0708/check_statement.py` | 0 | expression SHA-256 `35a5bcbc9cc3368a868a1e4d5c598c1cd0ca58420a5e067e621babcb867ae72d`; all four mutations distinguished |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0708/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `f6c9cc...a4fe`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups and exactly 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0708` | 0 | rank 749, planned, L0/rework-required, theorem incomplete |

The pre-existing untracked `Formalizations/Lean/.lake` canonical-cache materialization makes this
nonrelease evidence. This is statement-only evidence pending master acceptance; it does not claim
the theorem proof, anchor audit, obligation tree, validation, release, or theorem completion.
