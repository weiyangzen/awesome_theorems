# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Validation covers target-set consistency, dossier syntax and scoped intake invariants. The existing
Lean module is discovery input only and was not re-admitted by this phase; no kernel result or
machine-closure status is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0418` | exit 0; rank 73, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0418/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0418/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0418` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page, source conventions and errata,
canonical Lean elaboration, anchor/provenance audit, obligation registry, proof evidence, hermetic
replay, and independent review remain open. They do not invalidate this fail-closed planned intake.
