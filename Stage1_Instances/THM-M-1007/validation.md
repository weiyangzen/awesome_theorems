# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1007` | 0 | rank 287, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1007/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n -i '\\bsorry\\b|\\baxiom\\b|\\bplaceholder\\b|fake results' Stage1_Instances/THM-M-1007` | 1 | no forbidden proof shortcuts found (`rg` uses exit 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for the intake node. It introduces no Lean declaration, so a
kernel build would not validate an additional claim. Master acceptance and all dependent phases
remain outstanding.
