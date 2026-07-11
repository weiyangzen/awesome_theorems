# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

This is intake validation only; no Lean statement or kernel proof exists at this phase.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0145/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0145/task-dag.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0145` | exit 0; rank 320, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0145` | exit 0, no output |
| `rg -n "sorry|axiom|placeholder" Stage1_Instances/THM-M-0145` | exit 1, no matches |

Known failure: the primary-source theorem/page and therefore the exact formal statement remain
open by design for `S56-M-0145-STATEMENT`. This does not block truthful completion of the intake.
