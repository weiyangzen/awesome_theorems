# Statement validation record

Item: `S56-M-1082-STATEMENT`  
Base revision: `7c40b39aac30d12a21a2ca13ebe9406d4d57b383`

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned Lake environment. No
dependency was fetched, updated, cloned, or built. Mutation files are negative fixtures: success
means Lean emitted the expected elaboration/type error; Lean 4.29's frontend returned status 0 for
these diagnosed files, so the validation checked the emitted diagnostic text rather than treating
their process status as rejection evidence.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1082/Statement.lean` | 0 | exact target and checked `iff` wrapper elaborated; no output |
| `lake env lean ../../Stage1_Instances/THM-M-1082/StatementValidation.lean` | 0 | explicit fully elaborated declaration type printed and captured |
| `sha256sum /tmp/thm1082-print.txt` | 0 | elaborated print SHA-256 `26f4a571...ea592` |
| four `lake env lean ../../Stage1_Instances/THM-M-1082/mutations/*.lean` runs | 0 each | each emitted its expected error: missing `Module`, measure-domain mismatch, unknown escaped `I`, or missing `I.Nonempty` proof |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1082` | 0 | rank 524, planned, L0/rework-required, theorem incomplete |

## Status boundary

This is self-tested statement evidence pending master acceptance. The source record remains too
vague for `H0`; primary-source pinpointing belongs to the later anchor audit. Obligation freezing,
proof, hermetic replay, independent review, audit completion, and theorem completion remain open.
