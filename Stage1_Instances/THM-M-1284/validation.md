# Intake validation record

Base revision: `8046f7febfe203ec958fa24e111f6b730ad8393b`.

The exact commands and observed results are recorded below.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1284` | 0 | rank 455, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1284/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test "$(jq -r .item_id Stage1_Instances/THM-M-1284/intake.json)" = S56-M-1284-INTAKE` | 0 | dossier is bound to the assigned node |
| `test "$(jq -r .theorem_complete Stage1_Instances/THM-M-1284/intake.json)" = false` | 0 | dossier does not claim theorem completion |
| `git diff --check` | 0 | no whitespace errors |

This is intake-only evidence. No Lean declaration exists, so no kernel validation or theorem closure
is claimed.
