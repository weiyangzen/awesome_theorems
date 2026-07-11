# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1001` | 0 | rank 281, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1001/intake.json` | 0 | structured intake is valid JSON |
| dossier-local reference and prohibited-token checks (see worker receipt) | 0 | all four required dossier files present; no proof placeholders introduced |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel result is claimed. The exact-statement blocker is intentional and fail-closed.
