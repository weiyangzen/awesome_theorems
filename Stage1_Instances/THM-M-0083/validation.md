# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

The validation below establishes only membership and structural integrity of
this intake dossier. It does not validate or credit a Lean theorem.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0083` | 0 | rank 139, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0083/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-0083 -type f -name '*.lean' -print -quit \| grep -q .` | 1 | no Lean file or proof body was introduced by this intake-only node |
| `git diff --check -- Stage1_Instances/THM-M-0083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Master acceptance and all dependent phases remain outstanding.
