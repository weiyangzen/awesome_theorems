# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

This record covers dossier structure and manifest consistency only. No Lean declaration is added,
so no kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0130` | 0 | rank 26, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0130/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0130` | 0 | no whitespace errors |
| `rg -n "\bsorry\b\|\baxiom\b\|\badmit\b\|placeholder" Stage1_Instances/THM-M-0130` | 1 | no prohibited proof devices or placeholder markers found; exit 1 is `rg`'s no-match result |

Master acceptance and every dependent statement, audit, proof, validation, and release phase remain
outstanding.
