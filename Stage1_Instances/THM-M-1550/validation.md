# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

The validation below checks only the intake structure and repository membership. No new Lean
declaration is introduced, so no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1550` | 0 | rank 209; planned; L0/rework-required; historical artifacts unaccepted; theorem incomplete |

| `python3 -m json.tool Stage1_Instances/THM-M-1550/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_209.lean` | 0 | historical Lean discovery input exists |
| `test -f Docs/researches/math_theorems.md` | 0 | repository source row exists |
| `test -z "$(find Stage1_Instances/THM-M-1550 -name '*.lean' -print -quit)"` | 0 | intake introduces no Lean proof file or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-1550` | 0 | no whitespace errors |

Master acceptance and every dependent phase remain outstanding.
