# Intake validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0387/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry|axiom|placeholder" Stage1_Instances/THM-M-0387` | 0/1 | no matches at validation time (`rg` returns 1 for no matches) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is introduced and no
kernel-proof result is claimed. Master acceptance and every dependent phase remain outstanding.
