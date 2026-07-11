# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1293` | 0 | rank 173, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

| `python3 -m json.tool Stage1_Instances/THM-M-1293/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-1293` | 1 | no forbidden proof-construct terms found (`rg` uses 1 for no matches) |
| `test "$(rg -l 'THM-M-1293' Stage1_Instances/THM-M-1293 \| wc -l)" -eq 4` | 0 | all four dossier artifacts identify the assigned theorem |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node; this phase adds no Lean declaration and
claims no kernel closure. Master acceptance and all dependent phases remain outstanding.
