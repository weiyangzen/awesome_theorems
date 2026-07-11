# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

The commands below were run from the repository root. Their exact observed results are recorded
after the final self-test run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1266` | 0 | rank 162, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1266/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-1266 -type f -name '*.lean' -print -quit` | 0 | no Lean files exist in the intake dossier; no proof construct is introduced |
| `git diff --check -- Stage1_Instances/THM-M-1266` | 0 | no whitespace errors |

This is an intake-only structural validation. It neither checks a Lean target nor supplies kernel
evidence. Master acceptance and every dependent phase remain outstanding.
