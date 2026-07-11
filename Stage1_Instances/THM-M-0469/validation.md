# Intake validation record

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

The exact commands and observed results are recorded below. These checks validate an intake dossier,
not a Lean theorem.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0469` | 0 | rank 315, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0469/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder' Stage1_Instances/THM-M-0469/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | No prohibited tokens found (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0469 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors before manifest creation |

No Lean source is introduced in this phase, so a kernel invocation would not validate the unresolved
claim. Master acceptance and all dependent phases remain outstanding.
