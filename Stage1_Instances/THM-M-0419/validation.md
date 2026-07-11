# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | rank 74, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0419/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom' Stage1_Instances/THM-M-0419/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no matches (`rg` returns 1 when no lines match) |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is intake-only validation. No Lean declaration is introduced or accepted and no kernel-proof
result is claimed. Master acceptance and every dependent phase remain outstanding.
