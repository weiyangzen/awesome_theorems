# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

Commands run from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard, 1546-target coverage, and execution skill valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniformly L0 targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1149` | exit 0; rank 354, planned, L0/rework_required, theorem_complete false |

This validates membership and intake consistency only. No exact Lean target exists yet, so no Lean
compilation or kernel-proof claim is made. The known blocking gate is exact primary-source statement
identification.
