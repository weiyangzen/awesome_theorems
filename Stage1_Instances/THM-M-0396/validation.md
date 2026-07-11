# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

This record validates only the rev-5.6 intake dossier and its manifest identity.
It does not validate a Lean proposition or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0396` | 0 | Rank 9, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0396/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0396` | 0 | No whitespace errors |

Known failures: the exact source theorem and Lean statement are intentionally not
frozen in intake (`SRC-GAP-1`). No Lean build was run because this phase creates
no Lean declaration and claims no kernel closure.
