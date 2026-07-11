# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). The final
post-edit results are recorded below.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1051/intake.json >/dev/null` | 0 | JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1051/task-dag.json >/dev/null` | 0 | JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed for 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1051` | 0 | Rank 244, planned, L0/rework_required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1051` | 0 | No whitespace errors |

These are intake structural checks, not Lean proof validation. Exact statement elaboration,
source acceptance, and every theorem-completion gate remain open.
