# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

Validation is limited to manifest consistency, dossier structure, fail-closed scope, JSON syntax,
and whitespace. No exact Lean proposition exists yet, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1327` | exit 0; rank 489, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1327/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1327/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1327` | exit 0; no output |

Known downstream failures: primary-source inspection and independent review, exact variant and
conventions, canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic replay,
and release evidence remain open. These prevent theorem completion but not a planned intake.
