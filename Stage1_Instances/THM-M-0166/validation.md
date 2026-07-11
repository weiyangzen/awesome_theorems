# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0166` | 0 | rank 122; planned; L0/rework-required; historical artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0166/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `if rg -n '\\bsorry\\b\|\\baxiom\\b\|\\bplaceholder\\b' Stage1_Instances/THM-M-0166; then exit 7; else echo 'forbidden-token scan: no matches'; fi` | 0 | no forbidden proof-token matches |
| `rg -n 'THM-M-0166\|S56-M-0166-INTAKE' Stage1_Instances/THM-M-0166 >/dev/null` | 0 | dossier contains its theorem and item anchors |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for this intake-only node. No Lean source is introduced and no
kernel result is claimed. Master acceptance and all dependent phases remain outstanding.
