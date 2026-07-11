# Intake validation record

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1018/intake.json` | 0 | JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1018` | 0 | no whitespace errors |

These are intake-structure checks. No Lean command is applicable yet because this phase deliberately
does not assert an exact Lean declaration or expression. That open statement gate is recorded as
`M4`, not hidden as successful machine validation.
