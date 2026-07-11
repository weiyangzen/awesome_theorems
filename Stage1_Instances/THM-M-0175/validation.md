# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0175` | 0 | rank 124, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0175/intake.json >/dev/null` | 0 | dossier JSON syntax passed |
| `git diff --check -- Stage1_Instances/THM-M-0175` | 0 | no whitespace errors |

This is intake-only structural validation. No Lean file or exact formal expression exists, so a
kernel check would validate a substituted target rather than this root and is deliberately not
claimed.
