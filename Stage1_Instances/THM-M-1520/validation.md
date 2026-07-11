# Intake validation record

Base revision: `594dbb735284e7b81f51ce813a9c3200fd55f610`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | rank 189; planned; L0/rework-required; historical artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1520/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1520; test $? -eq 1` | 0 | no forbidden Lean proof devices or declarations found (`rg` returned 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

This is an intake-only node: no Lean declaration exists yet, so a kernel compilation would not
validate the claimed deliverable. Master acceptance and every dependent phase remain outstanding.
