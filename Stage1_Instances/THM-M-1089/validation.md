# Intake validation

Base revision: `93456b4e62d8d2ca82f56786d73e28e91b6d6120`.

Validation is limited to manifest consistency, dossier structure, planned-intake invariants, JSON
syntax, and whitespace. The source metadata does not identify an exact proposition, so there is no
canonical Lean expression to elaborate and no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1089` | exit 0; rank 531, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1089/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1089/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1089 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and inspection, canonical Lean
elaboration and mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent reviews. They prevent audit and theorem completion but do not invalidate a
truthful planned intake.
