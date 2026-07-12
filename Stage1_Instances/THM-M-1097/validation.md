# Intake validation

Base revision: `8875e7e449ea94d832c4e6dfa20c9d4e240bca79`.

Validation is limited to manifest consistency, dossier structure, scoped planned-intake
invariants, JSON syntax, and whitespace. The source label does not identify one theorem and no
canonical Lean expression exists, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1097` | exit 0; rank 537, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1097/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1097/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1097` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical Lean
elaboration and mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent release validation. They prevent audit and theorem completion but do not invalidate
this truthful planned intake.
