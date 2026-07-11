# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

The exact commands and results for this intake are recorded below. These checks validate target
membership and dossier structure only; no Lean declaration is introduced and no kernel closure is
claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0125/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\bsorry\b\|\baxiom\b\|\badmit\b' Stage1_Instances/THM-M-0125` | 1 | no forbidden proof escape terms found; `rg` exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0125 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Master acceptance and every dependent phase remain outstanding.
