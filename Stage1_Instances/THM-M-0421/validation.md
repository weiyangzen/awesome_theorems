# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Commands run from the worker clone on 2026-07-12:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0421` | exit 0; rank 76, planned, lane `hard_mathlib_anchor_and_wrapper`, theorem incomplete |

This validation is structural intake evidence only. No Lean declaration, source fidelity, proof,
kernel closure, or theorem completion is claimed. Known open gates are recorded in `intake.json`,
`scope_map.md`, and `source_statement_crosswalk.md`.
