# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 1546 uniform-L0 Lean 4 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1017` | 0 | rank 493, `planned`, lane `hard_mathlib_anchor_and_wrapper`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1017/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1017` | 0 | no whitespace errors |

These are intake-structural checks. No Lean command is applicable because choosing an exact Lean
expression before resolving the documented source ambiguity would substitute a theorem.
