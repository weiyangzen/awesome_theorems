# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

The exact commands and final results are recorded below after execution. These are structural
intake checks only; this phase introduces no Lean declaration and claims no kernel proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1177` | 0 | rank 377, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1177/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|axiom\|placeholder" Stage1_Instances/THM-M-1177/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1177` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. Master acceptance and every dependent
statement, source audit, obligation, proof, validation, and release phase remain outstanding.
