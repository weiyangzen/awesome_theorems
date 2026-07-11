# Intake validation record

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1020` | exit 0; rank 496, planned, L0, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1020/intake.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1020` | exit 0 |
| `test "$(find Stage1_Instances/THM-M-1020 -type f \| wc -l)" -eq 4` and placeholder scan | exit 0 before creation of the worker self-test manifest; four dossier files and no forbidden proof placeholders |

These are structural intake checks, not Lean elaboration or kernel evidence. No Lean target exists
to validate truthfully before source disambiguation.
