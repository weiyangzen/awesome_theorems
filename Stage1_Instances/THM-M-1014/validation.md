# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1014` | 0 | rank 293, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1014/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `if rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-1014/{README.md,intake.json,source_statement_crosswalk.md}; then exit 1; else test $? -eq 1; fi` | 0 | no forbidden proof escape terms found in the dossier content |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration or proof is
introduced, so kernel validation belongs to the dependent statement and proof phases. Master
acceptance and every dependent phase remain outstanding.
