# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` for 15 assurance groups, 1546 uniform-L0 targets, and execution skill |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1532` | 0 | rank 199, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1532/intake.json` | 0 | valid JSON |
| `find Stage1_Instances/THM-M-1532 -name '*.lean' -print` | 0 | no Lean proof files exist, so no proof shortcut can be present |
| `git diff --check -- Stage1_Instances/THM-M-1532` | 0 | no whitespace errors |

No Lean command is applicable: intake truthfully records that the source supplies no proposition to
elaborate. Statement elaboration is a dependent phase, and its blocker is explicit rather than
masked by a placeholder.
