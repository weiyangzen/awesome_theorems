# Intake validation record

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1021` | 0 | rank 497, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1021/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry|placeholder)\b' Stage1_Instances/THM-M-1021/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no matches (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1021` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. The dossier uses
the word `axiom` only when honestly describing the still-open trust audit; it
contains no Lean source or declaration. No kernel proof result is claimed.
