# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1015` | 0 | rank 294, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1015/intake.json >/dev/null` | 0 | pending validation run |
| dossier-local reference and forbidden-token check (Python) | 0 | four required files present, README references resolved, forbidden proof tokens absent |
| `git diff --check` | 0 | no whitespace errors |

These are structural intake checks only. No new Lean declaration or kernel-proof result is claimed.
Master acceptance and all dependent phases remain outstanding.
