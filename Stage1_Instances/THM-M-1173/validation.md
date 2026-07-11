# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1173` | 0 | rank 373; planned; L0/rework-required; source label untrusted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1173/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry|\baxiom\b|placeholder|fake result' Stage1_Instances/THM-M-1173` | 1 | no forbidden proof shortcuts or fake-result language found (`rg` exit 1 means no matches) |
| `rg -n 'THM-M-1173|S56-M-1173-INTAKE' Stage1_Instances/THM-M-1173` | 0 | dossier identity and owned-path references found |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It introduces no Lean declaration,
so kernel proof validation is not applicable. Exact statement, source acceptance, master acceptance,
and every dependent phase remain outstanding.
