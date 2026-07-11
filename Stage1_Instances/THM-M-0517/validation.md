# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0517` | 0 | rank 257, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0517/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0517 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is added or
credited. Exact elaboration, kernel evidence, master acceptance, and every dependent phase remain
outstanding.
