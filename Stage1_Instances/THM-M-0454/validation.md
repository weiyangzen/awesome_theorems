# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 1546 uniform-L0 Lean 4 targets and assurance structure accepted |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0454` | 0 | rank 303, planned, L0/rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0454/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0454` | 0 | no whitespace errors |

These are intake-structure checks only. No Lean command is applicable because the source statement
is absent; claiming an elaboration target would violate the exact-statement gate.
