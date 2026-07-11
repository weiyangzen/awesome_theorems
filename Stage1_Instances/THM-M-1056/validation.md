# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | rank 248, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1056/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1056` | 0 | no whitespace errors |

This is the smallest real intake validation. No Lean declaration is introduced, so no kernel proof
is claimed. Master acceptance and dependent phases remain outstanding.
