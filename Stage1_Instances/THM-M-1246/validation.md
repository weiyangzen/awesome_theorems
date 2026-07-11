# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

Commands run from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1246` | 0 | Confirmed rank 426, `planned`, `L0`, rework required, lane `hard_mathlib_anchor_and_wrapper` |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1246` | 0 | No whitespace errors |

These are intake-structure checks only. No Lean command is applicable because this phase deliberately
does not create or claim an elaborated formal statement. Source pinning, exact elaboration, kernel
closure, axiom inspection, and proof validation remain open dependent phases.
