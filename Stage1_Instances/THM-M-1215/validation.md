# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1215` | 0 | rank 407, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1215/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-1215 --glob '!validation.md'` | 1 | no proof-placeholder or axiom tokens found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1215` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. No Lean declaration is introduced, so
there is no kernel result. Exact statement elaboration, source acceptance, all dependent phases,
master acceptance, and theorem completion remain outstanding.
