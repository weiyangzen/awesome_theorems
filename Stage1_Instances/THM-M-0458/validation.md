# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Validation covers manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No Lean target exists yet, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0458` | exit 0; rank 306, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0458/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0458/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0458` | exit 0; no output |

Known downstream failures are the unresolved exact source/formula, canonical Lean elaboration,
anchor audit, obligation expansion, proof, hermetic replay, and independent review. These prevent
theorem completion but do not invalidate this fail-closed planned intake.
