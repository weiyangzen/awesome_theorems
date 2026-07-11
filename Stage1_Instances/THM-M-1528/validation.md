# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

The exact commands and results below validate only the intake structure and repository membership.
No Lean declaration is introduced, so no kernel proof is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1528` | 0 | rank 196, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1528/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder\|fake result' Stage1_Instances/THM-M-1528/{README.md,intake.json,source_statement_crosswalk.md} \|\| test $? -eq 1` | 0 | no forbidden proof devices or fake-result wording found (`rg` returned 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1528 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Master acceptance and all dependent phases remain outstanding.
