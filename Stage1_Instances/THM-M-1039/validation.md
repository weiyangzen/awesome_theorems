# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1039` | 0 | rank 232, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1039/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1039/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `test -f Stage1_Instances/THM-M-1039/README.md && test -f Stage1_Instances/THM-M-1039/scope-map.md && test -f Stage1_Instances/THM-M-1039/source-statement-crosswalk.md` | 0 | required dossier, scope map, and crosswalk exist |
| `test "$(find Stage1_Instances/THM-M-1039 -type f -name '*.lean' \| wc -l)" -eq 0` | 0 | intake introduced no Lean declaration |
| `git diff --check -- Stage1_Instances/THM-M-1039 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These checks establish intake structure and manifest consistency only. They are
not Lean elaboration, kernel evidence, source acceptance, or theorem completion.
Master acceptance and every dependent phase remain outstanding.

