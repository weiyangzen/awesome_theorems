# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | rank 35, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0112/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0112 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are intake-only structural checks. No Lean declaration is introduced, so this phase makes no
kernel, exact-type, axiom, or proof-closure claim. Master acceptance remains outstanding.
