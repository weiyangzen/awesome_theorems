# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0422` | 0 | rank 77, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0422/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom)\b\|placeholder' Stage1_Instances/THM-M-0422` (success means no output and `rg` exit 1) | 0 | wrapper check confirmed no matches; no prohibited proof construct occurs in the dossier |
| `for f in README.md intake.json source_statement_crosswalk.md validation.md; do test -f "Stage1_Instances/THM-M-0422/$f" \|\| exit 1; done` | 0 | all dossier-local references required by this intake exist |
| `git diff --check -- Stage1_Instances/THM-M-0422` | 0 | no whitespace errors |

This is an intake-only validation surface. No Lean declaration or proof is introduced, so no kernel
result is claimed. Master acceptance and every dependent phase remain outstanding.
