# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

Validation is limited to manifest/standard consistency, JSON syntax, scoped planned-intake
invariants, and whitespace. No exact Lean target is selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0571` | exit 0; rank 118, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0571/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0571/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0571` | exit 0; no output |

Known downstream failures: the primary-source theorem and local-index variant are not selected; the
canonical human claim and Lean expression are not frozen; source-page inspection, elaboration,
anchor audit, proof, hermetic replay, and independent review remain open. These prevent theorem
progress but do not invalidate this fail-closed planned intake.
