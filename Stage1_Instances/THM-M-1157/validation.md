# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

The validation below checks membership and dossier structure only. This phase introduces no Lean
declaration and makes no kernel-proof claim.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1157` | 0 | rank 360; planned; L0/rework-required; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1157/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\\b(sorry&#124;admit&#124;axiom)\\b' Stage1_Instances/THM-M-1157/{intake.json,README.md,source_statement_crosswalk.md}` | 1 | No forbidden proof constructs found (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1157 .stage1-worker-selftest.json` | 0 | No whitespace errors before receipt creation |

The first theorem gate remains blocked at source-statement identity. Master acceptance and every
dependent execution phase remain outstanding.
