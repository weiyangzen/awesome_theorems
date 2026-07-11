# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-0464 -name '*.lean' -print -quit` | 0 | no Lean files or proof bodies were introduced |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test manifest creation |

This is an intake-only node. No Lean declaration or proof body is introduced, so a kernel check
would not validate any claim made here. Master acceptance and all dependent phases remain open.
