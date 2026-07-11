# Intake validation record

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest consistent: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1034` | 0 | rank 227, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1034/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry|axiom|admit)\\b' Stage1_Instances/THM-M-1034/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof construct appears (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1034` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It introduces no Lean declaration and
claims no kernel result. Statement elaboration, source pinning, master acceptance, and all dependent
phases remain outstanding.
