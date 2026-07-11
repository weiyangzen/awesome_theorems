# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0426` | 0 | rank 80, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0426/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n --glob '!validation.md' 'sorry\|axiom\|placeholder\|fake result' Stage1_Instances/THM-M-0426` | 1 | no matches (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0426 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel result is claimed. Exact statement, master acceptance, and all dependent phases remain
outstanding.
