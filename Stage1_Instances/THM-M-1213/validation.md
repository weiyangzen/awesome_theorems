# Intake validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 1546 uniform-L0 targets and assurance structure validated |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1213` | 0 | rank 406, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1213/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1213` | 0 | no whitespace errors |

These are intake checks only. No Lean command is applicable because exact-statement selection is
deliberately deferred and no Lean declaration is claimed.
