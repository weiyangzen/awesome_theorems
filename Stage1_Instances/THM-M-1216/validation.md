# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1216` | 0 | rank 154, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1216/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry|admit)\b' Stage1_Instances/THM-M-1216` | 1 | no proof-placeholder tokens found (`rg` returns 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. No Lean declaration is introduced, so
there is no kernel result to report. Exact statement elaboration, source acceptance, all dependent
phases, node-specific master receipt, and theorem completion remain outstanding.
