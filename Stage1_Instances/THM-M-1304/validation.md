# Intake validation

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3f`.

Validation is limited to manifest consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No canonical Lean target exists, so no
elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1304` | exit 0; rank 472, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1304/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1304/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1304` | exit 0; no output |

Known downstream failures: primary-source identification and independent
review, exact statement, Lean elaboration, anchor audit, obligation registry,
proof, hermetic replay, and release validation remain open. These prevent
theorem completion but do not invalidate this planned intake.
