# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`

All commands ran from the worker clone root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0142/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0142` | 0 | Rank 317, planned, theorem incomplete, legacy artifacts unaccepted |
| `git diff --check -- Stage1_Instances/THM-M-0142` | 0 | No whitespace errors |

These are structural intake checks, not Lean kernel validation. No Lean target exists because the
source metadata does not identify an exact proposition. This intake is self-tested as a truthful
planned dossier; statement and theorem completion remain open.
