# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | rank 286; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1006/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test "$(python3 -c 'import json; print(json.load(open("Stage1_Instances/THM-M-1006/intake.json"))["item_id"])')" = S56-M-1006-INTAKE` | 0 | intake identity agrees with the assigned node |
| `test "$(find Stage1_Instances/THM-M-1006 -maxdepth 1 -type f \| wc -l)" -eq 4` | 0 | the four dossier artifacts exist in the owned path |
| forbidden-proof-token scan over `Stage1_Instances/THM-M-1006` | 0 | no forbidden proof-construction tokens found (the underlying `rg` no-match status is 1) |
| `git diff --check` | 0 | no whitespace errors |

This node introduces no Lean declaration, so a Lean kernel run would not
validate its intake deliverable. Master acceptance and all dependent phases remain outstanding.
