# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Validation is limited to manifest/standard consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. No exact Lean target is selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0570` | exit 0; rank 113, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0570/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0570/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0570` | exit 0; no output |

Known downstream failures: the primary-source theorem and variant are not selected; the canonical
human claim and Lean expression are not frozen; source-page inspection, elaboration, anchor audit,
proof, hermetic replay, and independent review remain open. These prevent theorem progress but do
not invalidate this fail-closed planned intake.
