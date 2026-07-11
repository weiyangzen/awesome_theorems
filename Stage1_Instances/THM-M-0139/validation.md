# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

The exact commands and results below validate intake structure only. No Lean declaration is
introduced, so no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0139` | 0 | rank 55, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0139/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\bsorry\\b|\\badmit\\b|\\baxiom\\b|placeholder|fake results' Stage1_Instances/THM-M-0139` | 1 | no prohibited proof shortcuts or result claims found; exit 1 means no matches |
| `git diff --check` | 0 | no whitespace errors |

Master acceptance and all dependent phases remain outstanding.
