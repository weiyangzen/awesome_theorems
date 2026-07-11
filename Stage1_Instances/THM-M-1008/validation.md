# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1008` | 0 | rank 288, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1008/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder' Stage1_Instances/THM-M-1008 -g '*.lean'` | 1 | no Lean files or forbidden proof-token matches (`rg` exit 1 means no match) |
| `test -f Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_288.lean` | 0 | historical candidate reference resolves |
| `rg -n 'THM-M-1008\|Hewitt-Savage' Docs/researches/math_theorems.md Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_288.lean >/dev/null` | 0 | repository source record and candidate contain the target anchors |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration was introduced,
so no kernel result is claimed. Master acceptance and every dependent phase remain outstanding.
