# Intake validation

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-1165` | 0 | rank 368, planned lifecycle, incomplete status confirmed |
| `python3 -m json.tool Stage1_Instances/THM-M-1165/intake.json` | 0 | structured intake parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1165/task_dag.json` | 0 | open task DAG parsed |
| `git diff --check -- Stage1_Instances/THM-M-1165` | 0 | no whitespace errors |

These checks validate a planned intake dossier only. Because the source does not provide an exact
truth-valued statement, there is no honest Lean expression to elaborate in this phase.
