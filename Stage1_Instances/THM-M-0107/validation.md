# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0107` | 0 | rank 31, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0107/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom\b|placeholder|fake results' Stage1_Instances/THM-M-0107/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof substitutes found; `rg` exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0107 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is intake-only validation. No Lean file is introduced, so there is no kernel build to report.
The statement, anchor-audit, proof, validation, release, and master-acceptance gates remain open.
