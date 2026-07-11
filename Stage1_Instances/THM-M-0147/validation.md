# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Preflight and narrow validation commands (run 2026-07-12 from repository root):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0147` | 0 | rank 322, planned, L0/rework-required, theorem incomplete |

No Lean command is applicable to this intake: no Lean expression is asserted, and the next phase is
blocked on exact source identity. Structural JSON parsing, scoped-content checks, and
`git diff --check` are run after artifact creation and recorded in the worker receipt.
