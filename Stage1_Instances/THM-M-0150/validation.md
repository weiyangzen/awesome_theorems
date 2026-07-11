# Intake validation record

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-0150` | 0 | rank 324, planned, L0, hard-mathlib-anchor lane, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0150/intake.json >/dev/null` | 0 | intake JSON parses |
| `test "$(rg -l 'THM-M-0150' Stage1_Instances/THM-M-0150 | wc -l)" -eq 3` | 0 | all three then-existing dossier files carried the theorem ID |
| `git diff --check -- Stage1_Instances/THM-M-0150` | 0 | no whitespace errors |

This is the smallest real intake validation. No Lean build was run because this phase intentionally
contains no Lean declaration. The first open gate is exact statement elaboration; consequently these
results provide dossier self-test evidence only and do not provide kernel evidence or theorem credit.
