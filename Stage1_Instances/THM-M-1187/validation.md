# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

This intake uses only structural validation because it introduces no Lean proposition.

| Command | Expected evidence |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | rev-5.6 standard and 1546-target projection pass |
| `python3 scripts/stage1_target.py check` | ordered manifest passes |
| `python3 scripts/stage1_target.py show THM-M-1187` | rank 382, planned, L0/rework-required, incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1187/intake.json >/dev/null` | intake JSON parses |
| `git diff --check -- Stage1_Instances/THM-M-1187` | owned artifacts have no whitespace errors |

Exact exits and output summaries are recorded in the worker self-test manifest after execution.
No kernel result is claimed; the first downstream failure is the exact statement gate.
