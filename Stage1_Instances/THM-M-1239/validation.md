# Intake validation

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

All commands were run from the worker clone root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1239/intake.json >/dev/null` | 0 | JSON syntax valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1239` | 0 | Rank 420; planned; L0/rework required; theorem incomplete |
| `rg -n "sorry\|axiom\|placeholder\|theorem_complete.*true" Stage1_Instances/THM-M-1239` | 1 | No forbidden proof/status marker found (expected no-match exit) |
| `git diff --check -- Stage1_Instances/THM-M-1239` | 0 | No whitespace errors |

These are structural intake checks only. No Lean target exists at this phase, so no elaboration or
kernel proof check is claimed. Exact statement identification remains blocked as documented in the
crosswalk; that is the planned intake boundary, not a failure of this intake deliverable.
