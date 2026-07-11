# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1037` | 0 | rank 230, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1037/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|axiom\|placeholder" Stage1_Instances/THM-M-1037/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden tokens (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1037 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This is an intake-only validation surface. No Lean declaration is introduced, so no kernel proof is
claimed. Exact statement, source acceptance, all dependent phases, and master acceptance remain open.
