# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0417` | 0 | rank 72, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0417/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-0417 --glob '!validation.md'` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for this intake-only node. No Lean declaration is introduced,
so no kernel check is claimed. Master acceptance and all dependent phases remain outstanding.
