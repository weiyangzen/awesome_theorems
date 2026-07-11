# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0997` | 0 | rank 277, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0997/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(sorry|admit|by_contra! false|^axiom )' Stage1_Instances/THM-M-0997` | 1 | no forbidden proof construct occurs (`rg` exit 1 means no match) |
| `rg -n 'source_statement_crosswalk.md|intake.json|validation.md' Stage1_Instances/THM-M-0997/README.md` | 0 | dossier-local artifacts are referenced by the scope surface |
| `git diff --check -- Stage1_Instances/THM-M-0997` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. This phase intentionally introduces no
Lean declaration, so there is no honest kernel command to run. Master acceptance and all dependent
statement, proof, and validation gates remain outstanding.
