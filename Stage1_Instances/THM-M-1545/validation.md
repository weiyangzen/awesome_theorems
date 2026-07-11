# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-1545` | 0 | Rank 204, planned lifecycle, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1545/intake.json >/dev/null` | 0 | Intake JSON parsed |
| dossier reference check recorded below | 0 | Required files and identifiers present; no forbidden proof placeholders |
| `git diff --check -- Stage1_Instances/THM-M-1545` | 0 | No whitespace errors |

These are intake checks only. No Lean build is credited because exact elaboration is assigned to the
dependent statement node.
