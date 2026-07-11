# Intake validation record

Base revision: `c67df8af765ae58e38b6c8d4ce37668f5a600c6b`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1244` | 0 | rank 425, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1244/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\|axiom\|placeholder' Stage1_Instances/THM-M-1244/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no forbidden proof tokens found (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1244 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is an intake-only node: it introduces no Lean declaration, so no kernel proof can truthfully be
tested. The checks establish target membership, standard consistency, structured dossier syntax,
and scoped artifact hygiene only. Master acceptance and every dependent phase remain outstanding.
