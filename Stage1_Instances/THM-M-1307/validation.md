# Intake validation record

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1307` | 0 | rank 166, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1307/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `find Stage1_Instances/THM-M-1307 -type f -name '*.lean' -print` | 0 | no Lean files or proof bodies are present in this intake |
| `git diff --check -- Stage1_Instances/THM-M-1307` | 0 | no whitespace errors |

This is intake-only. No Lean declaration is introduced, so no kernel theorem check is available or
claimed. Master acceptance and all dependent phases remain outstanding.
