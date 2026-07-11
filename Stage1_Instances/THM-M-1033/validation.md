# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1033` | 0 | rank 226, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1033/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|fake results" Stage1_Instances/THM-M-1033/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden-content matches (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1033 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel result is claimed. The statement phase, node-specific master acceptance, and all later
gates remain outstanding.
