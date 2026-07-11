# Intake validation

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Validation is limited to manifest/standard consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. No exact Lean target is frozen, so no elaboration or kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0555` | exit 0; rank 111, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0555/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0555/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0555` | exit 0; no output |

Known downstream failures: the exact source theorem, coefficient system, fibration hypotheses,
indexing, convergence, and Lean expression are not frozen. Primary-source inspection, anchor audit,
proof, hermetic replay, and independent review remain open. These prevent theorem completion but do
not invalidate a fail-closed planned intake.
