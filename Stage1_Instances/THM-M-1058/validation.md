# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | rank 250, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f Stage1_Instances/THM-M-1058/README.md && test -f Stage1_Instances/THM-M-1058/source_statement_crosswalk.md && test -f Stage1_Instances/THM-M-1058/validation.md` | 0 | required dossier files exist |
| `git diff --check -- Stage1_Instances/THM-M-1058` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It introduces no Lean declaration and
claims no kernel closure. Exact statement elaboration and master acceptance remain outstanding.
