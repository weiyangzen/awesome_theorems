# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

The following commands are the smallest real checks for this intake-only node. No Lean declaration
is introduced, so no kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | Rank 372, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1171/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1171` | 0 | No whitespace errors |

Master acceptance, exact-statement elaboration, source audit, and every proof/release gate remain
outstanding.
