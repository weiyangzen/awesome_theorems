# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-1166` | 0 | rank 369, planned lifecycle, and incomplete status confirmed |
| `python3 -m json.tool Stage1_Instances/THM-M-1166/intake.json` | 0 | pending post-write validation |
| `python3 -m json.tool Stage1_Instances/THM-M-1166/task_dag.json` | 0 | pending post-write validation |
| `git diff --check -- Stage1_Instances/THM-M-1166` | 0 | pending post-write validation |

These checks validate a planned intake dossier only. The catalogue supplies no truth-valued
statement, so there is no honest Lean expression to elaborate during this phase.
