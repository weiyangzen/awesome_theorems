# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1013` | 0 | rank 292, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1013/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(^|[^[:alnum:]_])(sorry|axiom)[[:space:]]+[[:alnum:]_]|placeholder|fake result' Stage1_Instances/THM-M-1013` | 1 | no prohibited proof construct or fabricated-result marker found (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1013 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is an intake-only node. No Lean declaration is introduced, so no kernel proof result is
claimed. Master acceptance and all dependent phases remain outstanding.
