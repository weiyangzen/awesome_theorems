# Intake validation

Validation is intentionally limited to the intake deliverable. It does not
elaborate a Lean statement or validate a proof.

Commands were run from the repository root on 2026-07-12 at base revision
`fe07aee0ce546497b6b69c8f7dcf910f374c09b1`:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1152` | 0 | rank 357, planned, L0/rework-required, theorem completion false |
| `python3 -m json.tool Stage1_Instances/THM-M-1152/intake.json` | 0 | JSON parsed successfully |
| `rg -n 'sorry\|admit\|axiom\|placeholder\|theorem_complete.: true' Stage1_Instances/THM-M-1152` | 0 | No matches (the shell command used `|| true` to make the empty-result check explicit) |
| `git diff --check -- Stage1_Instances/THM-M-1152` | 0 | No whitespace errors |

The source-status label remains untrusted. No network retrieval, source hash,
Lean elaboration, kernel check, or independent review occurred in this intake;
those are deliberately not claimed.
