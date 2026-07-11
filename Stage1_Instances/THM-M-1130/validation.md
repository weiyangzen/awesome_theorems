# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). Final post-edit results
are recorded here. These are intake structural checks, not Lean kernel validation.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1130/intake.json >/dev/null` | 0 | JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1130/task-dag.json >/dev/null` | 0 | JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed for 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1130` | 0 | Rank 335, planned, L0/rework_required, historical artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1130` | 0 | No whitespace errors |

No Lean declaration is introduced in this phase. Exact source selection, statement elaboration,
all proof gates, master acceptance, and theorem completion remain open.
