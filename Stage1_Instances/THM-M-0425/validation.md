# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0425` | 0 | rank 79, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0425/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0425` | 0 | no whitespace errors |

This is the smallest real validation for this intake-only node. No Lean
declaration is introduced, so a kernel build would not validate the dossier's
only claim. Master acceptance and all dependent phases remain outstanding.
