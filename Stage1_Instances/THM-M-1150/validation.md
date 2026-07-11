# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Commands run from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard, 1546-target coverage, and execution skill valid |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniformly L0 targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1150` | exit 0; rank 355, planned, L0/rework_required, theorem_complete false |

This validates membership and dossier structure at intake only. No Lean target exists yet, so no
Lean compilation or kernel-proof claim is made. The known blocking gate is exact primary-source
statement identification.
