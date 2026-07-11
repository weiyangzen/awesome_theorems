# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Commands run from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0461` | 0 | rank 309, `planned`, `L0`, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0461/intake.json` | 0 | valid JSON |
| dossier-local reference check (documented below) | 0 | all declared public merge targets exist; identity fields match |
| `git diff --check -- Stage1_Instances/THM-M-0461 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The dossier-local check used Python's standard JSON and path APIs to assert the theorem ID, item ID,
`planned` lifecycle, incomplete status, and existence of every `public_merge_targets` path. These are
structural intake checks, not Lean kernel evidence. No Lean command is applicable because refusing
to invent a formal target is the recorded exact-statement boundary.
