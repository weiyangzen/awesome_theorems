# Intake validation record

Base revision: `9c650bd6aac0dca129c8bc8ac01e0d7432669386`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0999` | 0 | rank 279, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0999/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n "sorry\|axiom\|placeholder\|admit" Stage1_Instances/THM-M-0999 --glob '!validation.md'` | 1 | No prohibited-token matches (`rg` uses exit 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0999` | 0 | No whitespace errors |

This is an intake-only validation surface. No Lean file or declaration is introduced, so no kernel
result is claimed. Exact-source identification, master acceptance, and every dependent phase remain
outstanding.
