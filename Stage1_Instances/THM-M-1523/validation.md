# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1523` | 0 | rank 191, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1523/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1523` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration exists because
the source statement is not yet proposition-level; therefore no elaboration or kernel-proof result
is claimed. The exact-statement gate is the recorded blocker for dependent work.
