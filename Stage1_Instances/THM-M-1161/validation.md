# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; planned; L0/rework-required; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json` | 0 | No whitespace errors |
| `rg -n '\\bsorry\\b|\\baxiom\\b|placeholder|fake result' Stage1_Instances/THM-M-1161` | 1 | No forbidden-content matches (`rg` uses exit 1 for no matches) |

These are structural intake checks only. No Lean declaration was introduced, so there is no kernel
proof result to report. Exact elaboration and all downstream acceptance gates remain open.
