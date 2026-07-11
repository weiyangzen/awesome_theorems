# Intake validation

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

The preflight and scoped checks were run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1207` | 0 | rank 400, planned, L0/rework-required, hard anchor/wrapper lane |
| `python3 -m json.tool Stage1_Instances/THM-M-1207/intake.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1207` | 0 | no whitespace errors |

No Lean command is claimed: the intake deliberately records that the source metadata does not yet
determine a proposition. Lean elaboration belongs to the dependent statement phase after source
disambiguation. Known failure/open gate: exact statement and primary-source premise crosswalk remain
open (`H4/M4`), so this receipt supports intake self-test only and not theorem completion.
