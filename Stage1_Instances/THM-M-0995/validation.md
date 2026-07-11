# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0995` | 0 | rank 275, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0995/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorryAx|\bsorry\b|\badmit\b' Stage1_Instances/THM-M-0995/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof token found in substantive intake artifacts (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0995 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is introduced and no
kernel-proof result is claimed. Master acceptance and every dependent phase remain outstanding.
