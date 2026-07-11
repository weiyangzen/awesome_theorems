# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1046` | 0 | rank 239, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1046/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n -i '\\bsorry\\b\|\\baxiom\\b\|\\bplaceholder\\b' Stage1_Instances/THM-M-1046` | 1 | no forbidden proof escape terms found (`rg` exit 1 means no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for the intake-only phase. It establishes target membership,
standard consistency, JSON syntax, and dossier hygiene. No Lean declaration is introduced, so no
kernel result is claimed. Statement elaboration, source acceptance, master acceptance, and all
dependent phases remain outstanding.
