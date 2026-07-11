# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0006` | 0 | rank 95, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool` on dossier JSON files | 0 | structured intake and task DAG are valid JSON |
| dossier local-reference and forbidden-marker checks | 0 | all referenced local artifacts exist; no forbidden proof escape marker occurs |
| `git diff --check` | 0 | no whitespace errors |

These checks validate intake structure only. No new Lean declaration was introduced, so no kernel
proof result is claimed.
