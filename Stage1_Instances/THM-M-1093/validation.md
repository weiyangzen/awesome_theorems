# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

This record is completed by the commands below after dossier creation. The scope is intake-only:
no Lean declaration is introduced or credited, and no kernel-proof result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1093` | 0 | rank 217, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1093/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom)\b' Stage1_Instances/THM-M-1093` | 1 | no forbidden Lean proof declarations found (`rg` exit 1 means no matches) |
| `rg -n 'THM-M-1093\|StatementShape\|source_statement_crosswalk.md\|validation.md' Stage1_Instances/THM-M-1093` | 0 | dossier-local identifiers and referenced artifacts are present |
| `git diff --check` | 0 | no whitespace errors |

These checks self-test the assigned intake deliverable only. Primary-source acceptance, exact Lean
elaboration, theorem proof, master receipt acceptance, and all downstream nodes remain outstanding.
