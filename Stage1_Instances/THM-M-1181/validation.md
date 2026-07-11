# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

This record is completed by the validation run for this intake. It covers structure only: no Lean
declaration is introduced and no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1181` | 0 | rank 149, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1181/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(^\\|[^A-Za-z])(sorry\\|axiom)([^A-Za-z]\\|$)\\|placeholder\\|fake result\\|fake proof' Stage1_Instances/THM-M-1181/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof tokens found (`rg` exit 1 means no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1181 .stage1-worker-selftest.json` | 0 | no whitespace errors before receipt creation |

Master acceptance and all dependent statement, audit, proof, validation, and release phases remain
outstanding.
