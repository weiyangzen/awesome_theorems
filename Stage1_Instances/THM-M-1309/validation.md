# Intake validation

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3`.

The worker ran the following commands from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 Lean 4 targets and the execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1309` | exit 0; rank 476, planned, lane `hard_mathlib_anchor_and_wrapper`, theorem incomplete |

These checks validate manifest membership and the repository baseline only. Dossier JSON syntax,
local reference integrity, and whitespace checks are recorded by the worker self-test after creation.
No Lean command is applicable at intake because no Lean expression is claimed.
