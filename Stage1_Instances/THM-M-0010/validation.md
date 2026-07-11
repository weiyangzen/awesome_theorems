# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0010` | 0 | rank 103, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0010/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|\bplaceholder\b' Stage1_Instances/THM-M-0010` | 1 | no forbidden proof constructs found; exit 1 means no matches |
| `git diff --check` | 0 | no whitespace errors |

These are the smallest real checks for this intake-only node. No Lean declaration is introduced,
so no kernel result is claimed. Master acceptance and every dependent phase remain outstanding.
