# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | rank 238, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test "$(find Stage1_Instances/THM-M-1045 -maxdepth 1 -type f \| wc -l)" -eq 4` | 0 | all four dossier artifacts exist |
| `! rg -n "\\bsorry\\b\|\\baxiom\\b\|\\bplaceholder\\b\|fake result" Stage1_Instances/THM-M-1045/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | no forbidden proof devices or fake-result markers found |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No kernel theorem is introduced, and
no proof or theorem-completion result is claimed. Master acceptance and all dependent phases remain
outstanding.
