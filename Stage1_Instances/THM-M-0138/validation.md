# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0138` | 0 | rank 54, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0138/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\\|axiom\\|placeholder\\|fake result' Stage1_Instances/THM-M-0138/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof mechanism or fake-result wording found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0138 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test-manifest creation; rerun afterward |

These are the smallest real checks for an intake-only node. This phase introduces no Lean
declaration and claims no kernel result. Master acceptance and all dependent phases remain open.
