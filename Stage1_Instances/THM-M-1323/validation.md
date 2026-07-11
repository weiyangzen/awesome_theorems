# Intake validation record

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1323` | 0 | rank 485, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1323/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1323` | 0 | no whitespace errors |

This is the smallest real validation for the intake node. No Lean source or theorem is introduced,
so no elaboration or kernel closure is claimed. Exact-source acceptance, master acceptance, and all
dependent phases remain outstanding.
