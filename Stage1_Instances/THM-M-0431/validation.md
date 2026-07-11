# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0431` | 0 | rank 59, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0431/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)' Stage1_Instances/THM-M-0431` | 1 | no prohibited Lean proof declarations found; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0431 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is an intake-only validation surface. No Lean declaration is introduced, so there is no kernel
proof to compile or credit. Master acceptance and every dependent phase remain outstanding.
