# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Exact command results are recorded after the validation run below. These checks validate only the
intake artifact structure; no Lean target exists yet and no kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | rank 40, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0121/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `if rg -n '\\b(sorry\|axiom\|placeholder)\\b' Stage1_Instances/THM-M-0121; then exit 2; else test $? -eq 1; fi` | 0 | no forbidden proof-token matches (`rg` returned 1, converted to successful absence check) |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for the intake-only node. Master acceptance and every
dependent phase remain outstanding.
