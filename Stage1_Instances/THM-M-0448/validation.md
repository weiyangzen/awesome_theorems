# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Validation is limited to manifest/standard consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. The exact Lean target is intentionally not selected in this phase, so
no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0448` | exit 0; rank 62, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0448/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0448/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0448` | exit 0; no output |

Known downstream failures: the exact primary-source theorem, normalization, binders, and Lean
expression are not frozen. Source review, anchor audit, elaboration, proof, hermetic replay, and
independent verification remain open. These failures prevent theorem completion but do not
invalidate a fail-closed planned intake.
