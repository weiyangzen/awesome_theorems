# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | rank 158, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry\|axiom\|placeholder)\\b' Stage1_Instances/THM-M-1234` | 1 | no forbidden proof escape terms found (`rg` returns 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel-proof result is claimed. Master acceptance and every dependent phase remain open.
