# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON,
and whitespace. No canonical Lean expression exists, so no kernel result is claimed.

The exact commands and results from this worker run are recorded below.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard validator passed |
| `python3 scripts/stage1_target.py check` | exit 0; target manifest check passed |
| `python3 scripts/stage1_target.py show THM-M-0457` | exit 0; rank 305, L0/rework required, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0457/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0457/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0457` | exit 0; no output |

Known downstream failures: a unique source proposition, exact edition/theorem/page inspection,
canonical Lean elaboration, anchor audit, proof, hermetic replay, and independent review remain
open. These prevent theorem completion but do not invalidate this fail-closed planned intake.
