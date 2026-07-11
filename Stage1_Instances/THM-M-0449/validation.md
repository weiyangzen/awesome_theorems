# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0449` | 0 | rank 63, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0449/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|admit\|sorryAx\|\\baxiom\\b\|placeholder\|fake results" Stage1_Instances/THM-M-0449` | 1 | no forbidden proof or result markers found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0449 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This intake validation establishes only a well-formed planned dossier and a truthful source-identity
blocker. It establishes no exact Lean statement and no kernel proof. Master acceptance and all
dependent phases remain outstanding.
