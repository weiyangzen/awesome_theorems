# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The preflight and scoped structural checks were run from the repository root on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0414` | exit 0; rank 69, planned, L0, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0414/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0414/task-dag.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0414` | exit 0 |

This is intake-only validation. No Lean build or kernel-proof validation is claimed because this
phase intentionally creates a planned dossier and does not freeze an exact Lean declaration.
