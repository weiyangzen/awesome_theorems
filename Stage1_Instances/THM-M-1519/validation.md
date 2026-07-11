# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1519` | 0 | rank 188, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1519/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n "sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-1519` | 1 | no forbidden Lean proof escape matches; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-1519 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration is introduced,
so no kernel proof or exact-type check is claimed. Exact-statement selection and every dependent
phase remain open, as does master acceptance.
