# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1270` | 0 | rank 163, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1270 .stage1-worker-selftest.json` | 0 | No whitespace errors in the owned dossier or worker receipt |

This is an intake-only node. No Lean declaration is introduced and no elaboration, kernel proof,
trust audit, or theorem-completion result is claimed. Master acceptance and every dependent phase
remain outstanding.
