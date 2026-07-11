# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1552` | 0 | rank 211, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1552/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|placeholder\|fake result' Stage1_Instances/THM-M-1552/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no prohibited proof devices or result claims found (`rg` returns 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the narrowest real validation for an intake-only node. No Lean declaration was introduced,
so there is no kernel claim to test. The source-identification blocker is part of the truthful intake
result; it blocks the dependent statement phase, not this dossier's structural self-test.
