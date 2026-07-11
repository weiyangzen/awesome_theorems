# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The validation commands below were run from the repository root after creating this dossier.
Their exact results are recorded here; none checks a Lean theorem because intake introduces no
Lean declaration.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: assurance groups and frozen 1546-target uniform-L0 standard agree |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0423` | 0 | rank 67, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0423/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -z "$(find Stage1_Instances/THM-M-0423 -name '*.lean' -print -quit)"` | 0 | intake adds no Lean proof surface, hence no proof hole or new declaration |
| `git diff --check -- Stage1_Instances/THM-M-0423` | 0 | no whitespace errors in the owned path |

This is the smallest real validation for an intake-only node. Master acceptance and all dependent
statement, audit, proof, validation, and release phases remain outstanding.
