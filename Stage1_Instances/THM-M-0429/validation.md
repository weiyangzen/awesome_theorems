# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0429` | 0 | rank 82, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0429/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\\b(sorry|axiom)\\b' Stage1_Instances/THM-M-0429 --glob '!validation.md'` | 1 | No forbidden proof escape appears in deliverables; `rg` exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0429` | 0 | No whitespace errors in the owned path |

This is the smallest real validation for an intake-only node. It introduces no Lean declaration and
claims no kernel result. Master acceptance and every dependent phase remain outstanding.
