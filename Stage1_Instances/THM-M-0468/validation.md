# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

All commands were run from the repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0468/intake.json` | 0 | JSON parsed successfully |
| `rg -n 'sorry\|admit\|axiom\|placeholder\|theorem_complete.: true' Stage1_Instances/THM-M-0468` | 0 | One prose occurrence of `axiom` in the intentionally open TCB boundary; no proof source, placeholder declaration, or completion claim |
| `git diff --check -- Stage1_Instances/THM-M-0468` | 0 | no whitespace errors |

This is dossier validation, not Lean theorem validation. There is deliberately no
Lean file or declaration in the intake phase, so these results do not establish
statement elaboration, kernel closure, source acceptance, or theorem completion.

