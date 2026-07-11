# Intake validation

Base revision: `056367be3b1cb2e101200085ec5a5fdff670d16b`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. The scheduler-owned generated blueprint and execution DAG were already
modified in this automation clone and were not edited by this worker. No Lean expression has been
frozen, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1241` | exit 0; rank 422, no legacy slot, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1241` | exit 0; no output |

Known downstream failures: exact primary-source inspection and independent review, selection of a
single theorem variant, canonical Lean elaboration, anchor audit, obligation registry, proof,
hermetic validation, and release remain open. They prevent theorem completion but do not invalidate
this fail-closed planned intake.
