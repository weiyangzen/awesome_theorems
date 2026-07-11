# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 1546 uniform-L0 Lean 4 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | rank 78, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom' Stage1_Instances/THM-M-0424 -g '!validation.md'` | 1 | no matches (`rg` returns 1 when it finds none) |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is an intake-only validation surface. It introduces no Lean declaration, so no kernel result is
claimed. Exact statement elaboration, source acceptance, node receipt, and master acceptance remain
open.
