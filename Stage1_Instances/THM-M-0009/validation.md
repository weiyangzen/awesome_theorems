# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Commands run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0009` | 0 | Rank 102, planned, L0/rework-required, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0009/instance.json` | 0 | JSON parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0009/task-dag.json` | 0 | JSON parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0009` | 0 | No whitespace errors. |

This validates the planned intake artifact only. No Lean command is credited because statement
elaboration belongs to the dependent statement node and the canonical proposition is intentionally
not frozen here.
