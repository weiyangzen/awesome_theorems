# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

Commands are run from the repository root. This is structural intake evidence only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1158` | 0 | rank 361; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1158/intake.json` | 0 | valid JSON |
| dossier reference check (see worker self-test command) | 0 | required files and item/theorem IDs present |
| `git diff --check -- Stage1_Instances/THM-M-1158` | 0 | no whitespace errors |

Known limitation: no Lean command is meaningful because the upstream metadata does not
identify an exact proposition. This is recorded as `M4`, not disguised by elaborating a
chosen substitute.
