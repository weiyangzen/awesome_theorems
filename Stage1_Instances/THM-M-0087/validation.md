# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0087` | 0 | rank 133, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0087/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-0087 -type f -name '*.lean' -print -quit` | 0 | no Lean file was introduced by this intake |
| `test -f Stage1_Instances/THM-M-0087/README.md && test -f Stage1_Instances/THM-M-0087/scope-map.md && test -f Stage1_Instances/THM-M-0087/source-statement-crosswalk.md` | 0 | all required intake surfaces exist |
| `git diff --check -- Stage1_Instances/THM-M-0087 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is an intake-only structural validation. It introduces no Lean declaration
and claims no kernel evidence. Master acceptance and all dependent phases remain
outstanding.
