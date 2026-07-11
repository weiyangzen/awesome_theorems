# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

Validation covers manifest membership, repository consistency, planned-dossier structure, scoped
intake invariants, JSON syntax, and whitespace. There is intentionally no Lean command: the exact
source proposition and canonical Lean expression remain open, so kernel validation would be false
precision.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1252` | exit 0; rank 431, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1252/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1252/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1252` | exit 0; no output |

Known downstream failures are exact primary-source identification, exact statement selection and
Lean elaboration, anchor audit, obligation expansion, proof, hermetic validation, and independent
review. They prevent theorem completion but not a fail-closed planned intake.
