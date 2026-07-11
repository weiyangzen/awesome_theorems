# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1527` | 0 | rank 195, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1527/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '"(sorry|axiom|placeholder)"' Stage1_Instances/THM-M-1527/intake.json` | 1 | no forbidden structured proof construct found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1527 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean theorem is introduced, so a
Lean kernel build would not validate the deliverable. Master acceptance and every dependent phase
remain outstanding.
