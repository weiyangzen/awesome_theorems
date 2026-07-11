# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1274` | 0 | rank 447, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1274/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|axiom\|place" Stage1_Instances/THM-M-1274` | 1 | no forbidden proof constructs found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1274 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is intake-only validation. No Lean declaration is introduced, so no kernel result is claimed.
The exact statement gate and master acceptance remain outstanding.
