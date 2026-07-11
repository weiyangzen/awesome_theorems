# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. No canonical Lean target exists yet, so no elaboration or kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1227` | exit 0; rank 416, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1227/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1227/task-dag.json` | exit 0 |
| scoped Python intake assertions (command in worker self-test manifest) | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1227` | exit 0; no output |

Known downstream failures: exact primary-source inspection, canonical Lean elaboration, anchor
audit, obligation expansion, proof, hermetic replay, and independent review remain open. These
prevent theorem completion but do not invalidate the fail-closed planned intake.
