# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0427` | 0 | rank 81, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0427/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-0427` | 1 | no forbidden-token matches (`rg` exit 1 means no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for the intake node. No Lean declaration was introduced, so a
Lean build would not validate additional owned proof content. Master acceptance and all dependent
phases remain outstanding.
