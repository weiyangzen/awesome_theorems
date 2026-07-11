# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1237` | 0 | rank 175, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1237/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'sorry\\b|\\baxiom\\b|placeholder|fake result' README.md intake.json source_statement_crosswalk.md` (from the owned directory) | 1 | no forbidden-content matches (`rg` uses exit 1 for no matches) |
| `test -f` for all four owned files, then `rg -q` for the item and theorem IDs | 0 | required owned artifacts and identifiers are present |
| `git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test manifest creation |

This is an intake-only validation surface. It introduces no Lean theorem and makes no kernel-proof
claim. Master acceptance and every dependent phase remain outstanding.
