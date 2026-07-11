# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1182` | 0 | rank 150, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1182/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom\b|placeholder|fake result' Stage1_Instances/THM-M-1182` | 1 | no forbidden proof escape or fabricated-result marker found (`rg` exit 1 means no match) |
| `test -f Stage1_Instances/THM-M-1182/README.md -a -f Stage1_Instances/THM-M-1182/source_statement_crosswalk.md -a -f Stage1_Instances/THM-M-1182/validation.md` | 0 | required dossier surfaces exist |
| `git diff --check` | 0 | no whitespace errors |

This is intake-only validation: it establishes no exact Lean target and no kernel-proof result.
Master acceptance and every dependent phase remain outstanding.
