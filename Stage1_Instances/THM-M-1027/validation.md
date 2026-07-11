# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1027` | 0 | rank 218, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1027/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(^|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]|$)\|^[[:space:]]*axiom[[:space:]]\|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-1027/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof construct or completion claim found (`rg` exit 1 means no match) |
| `rg -n 'THM-M-1027\|S56-M-1027-INTAKE' Stage1_Instances/THM-M-1027` | 0 | dossier contains the assigned theorem and item identifiers |
| `git diff --check -- Stage1_Instances/THM-M-1027 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration was introduced,
so no kernel-proof result is claimed. Master acceptance and every dependent phase remain open.
