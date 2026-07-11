# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

Commands run from the repository root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1324` | 0 | Rank 486, planned, L0/rework-required, hard anchor/wrapper lane |
| `python3 -m json.tool Stage1_Instances/THM-M-1324/intake.json` | 0 | JSON syntax valid |
| `git diff --check -- Stage1_Instances/THM-M-1324` | 0 | No whitespace errors |

These checks validate intake structure and scope consistency only. No Lean build is applicable
because this phase deliberately has no canonical Lean declaration; this is the first failed gate.
