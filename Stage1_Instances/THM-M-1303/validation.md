# Intake validation record

Base revision: `1a8797e69ff09d2b1e4aa81a7b7e8d2b14e56892`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1303` | 0 | rank 471, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1303/intake.json >/dev/null` | 0 | intake JSON parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1303/task-dag.json >/dev/null` | 0 | task DAG JSON parses |
| `git diff --check -- Stage1_Instances/THM-M-1303 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are intake-only structural checks. No Lean declaration exists in this dossier, so no kernel
result is claimed. Exact statement identification and all dependent gates remain open.

