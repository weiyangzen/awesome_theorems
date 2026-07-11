# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0182` | 0 | rank 128, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0182/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test $(find Stage1_Instances/THM-M-0182 -maxdepth 1 -type f \| wc -l) -eq 4` | 0 | the four required dossier surfaces exist |
| `! rg -n '\b(sorry\|axiom\|admit)\b' Stage1_Instances/THM-M-0182/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | no prohibited proof escape appears in substantive intake artifacts |
| `! rg -n '/home/\|\.cron/' Stage1_Instances/THM-M-0182/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | no private absolute path or automation path leaks into substantive intake artifacts |
| `git diff --check` | 0 | no whitespace errors |

These preflight results validate manifest membership and repository-standard consistency only. The
No Lean declaration is introduced by this intake node, so no kernel-proof result is claimed. Master
acceptance and all dependent phases remain outstanding.
