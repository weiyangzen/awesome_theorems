# Intake validation

Date: 2026-07-12 (Asia/Shanghai)

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0397` | 0 | rank 10, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0397/intake.json` | 0 | Parsed the owned structured intake |
| `git diff --check -- Stage1_Instances/THM-M-0397` | 0 | No whitespace errors in the owned path |

Scope: dossier and intake consistency only. No Lean declaration was created or
credited in this phase, so a Lean build would not validate the missing exact claim.
