# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1400` | 0 | rank 297, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1400/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n -g '!validation.md' "sorry\|axiom" Stage1_Instances/THM-M-1400` | 1 | no matches (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1400` | 0 | no whitespace errors |

This is the smallest real validation surface for an intake-only node. No Lean theorem is introduced,
so a Lean kernel check would not validate any additional claim. Master acceptance and all dependent
phases remain outstanding.
