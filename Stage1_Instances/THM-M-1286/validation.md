# Intake validation record

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | rank 457, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry\|axiom\|placeholder)\\b' Stage1_Instances/THM-M-1286` | 1 | no forbidden proof-device terms found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1286` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration or proof is
introduced, so kernel compilation is not applicable. Exact statement elaboration, source acceptance,
master acceptance, and all dependent phases remain outstanding.
