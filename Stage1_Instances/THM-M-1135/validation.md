# Intake validation record

Base revision: `6d9732600c7da75d9b55873adc3303cf64bd77f2`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1135` | 0 | rank 340, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1135/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(s[o]rry\|a[x]iom\|place[h]older)\b' Stage1_Instances/THM-M-1135` | 1 | no forbidden proof tokens found (`rg` exit 1 means no matches) |
| `rg -n 'THM-M-1135\|S56-M-1135-INTAKE' Stage1_Instances/THM-M-1135` | 0 | dossier contains the expected theorem and item references |
| `git diff --check` | 0 | no whitespace errors |

The dossier-local JSON, forbidden-token, reference, and whitespace checks are recorded after their
final run below. This is an intake-only node: it introduces no Lean declaration, so no kernel result
is claimed. Master acceptance and all dependent phases remain outstanding.
