# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0004` | 0 | Rank 99, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0004/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\\bsorry\\b|\\baxiom\\b|\\bplaceholder\\b' Stage1_Instances/THM-M-0004` | 1 | No forbidden tokens; `rg` returns 1 for no matches |
| `git diff --check -- Stage1_Instances/THM-M-0004 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This phase introduces no Lean declaration. Structural and documentary checks are therefore the
smallest validation that tests the intake deliverable. Kernel validation belongs to the dependent
statement phase; master acceptance remains outstanding.
