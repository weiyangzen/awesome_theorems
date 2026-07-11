# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0326` | 0 | rank 215, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0326/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|fake results' Stage1_Instances/THM-M-0326` | 1 | no forbidden-token matches; exit 1 is ripgrep's no-match result |
| `git diff --check` | 0 | no whitespace errors |

This is the narrow real validation for an intake-only node. It introduces no Lean declaration and
therefore makes no kernel-closure claim. Exact statement elaboration, source acceptance, all later
phases, a node-specific receipt, and master acceptance remain outstanding.
