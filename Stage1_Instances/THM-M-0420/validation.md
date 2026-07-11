# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The validation commands and results below are for this intake node only. No Lean declaration is
introduced, so no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0420` | 0 | rank 75, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0420/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\\bsorry\\b|\\badmit\\b|sorryAx|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0420/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | No Lean proof escape or axiom declaration found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0420 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

Master acceptance, exact statement elaboration, source acceptance, and all theorem-completion gates
remain outstanding.
