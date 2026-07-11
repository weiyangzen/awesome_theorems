# Intake validation record

Base revision: `6d9732600c7da75d9b55873adc3303cf64bd77f2`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1129` | 0 | rank 334, planned, hard-mathlib-anchor-and-wrapper lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1129/intake.json` | 0 | valid JSON |
| `git diff --check` | 0 | no whitespace errors |

The narrow validation is intentionally structural: intake creates no Lean declaration and therefore
has no honest kernel build target. Source pinning, exact elaboration, and Lean validation are gates
for dependent phases, not evidence supplied here.
