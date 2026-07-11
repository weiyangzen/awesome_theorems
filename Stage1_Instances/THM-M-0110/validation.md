# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0110` | 0 | rank 34, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0110/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|fake result' Stage1_Instances/THM-M-0110/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden-token matches (`rg` uses exit 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

These checks cover only manifest membership, standard consistency, JSON syntax, forbidden-token
absence, and whitespace. No Lean declaration is introduced by this intake and no kernel result is
claimed. Master acceptance and all dependent phases remain outstanding.
