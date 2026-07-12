# Intake validation

Base revision: `93456b4e62d8d2ca82f56786d73e28e91b6d6120`.

Validation is limited to manifest consistency, dossier structure, scoped planned-intake
invariants, JSON syntax, and whitespace. There is no canonical Lean expression yet, so no Lean
elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1088` | exit 0; rank 530, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1088/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1088/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source inspection, canonical Lean elaboration and mutation
tests, formal-candidate audit, obligation registry, proof, hermetic replay, and independent reviews
remain open. They prevent audit and theorem completion but do not invalidate this truthful planned
intake.
