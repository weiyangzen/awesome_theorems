# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Validation is limited to manifest consistency, dossier structure, fail-closed intake invariants, and
whitespace. No canonical Lean expression exists yet, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0151` | exit 0; rank 325, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0151/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0151/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0151` | exit 0; no output |

Known downstream failures: primary-source disambiguation and inspection, exact statement and Lean
elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent review are
open. They prevent theorem completion but do not invalidate this planned intake.
