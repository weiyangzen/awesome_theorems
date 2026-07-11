# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1201/intake.json >/dev/null` | 0 | intake JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-1201` | 0 | rank 395, planned, theorem incomplete |
| `rg -n 'THM-M-1201\|S56-M-1201-INTAKE' Stage1_Instances/THM-M-1201` | 0 | dossier identifiers and local references found |
| `git diff --check -- Stage1_Instances/THM-M-1201` | 0 | no whitespace errors |

These are intake-only structural checks. No Lean target exists because the source metadata does not
identify an exact theorem; consequently no elaboration, kernel proof, or theorem completion is
claimed. Known failure: the dependent statement gate is blocked on primary-source disambiguation.
