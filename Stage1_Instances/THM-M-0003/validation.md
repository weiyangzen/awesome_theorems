# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0003` | 0 | Rank 98, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0003/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `rg -n '\bsorry\b|\baxiom\b|\bplaceholder\b' Stage1_Instances/THM-M-0003/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | No forbidden tokens; `rg` returns 1 for no matches |
| `git diff --check -- Stage1_Instances/THM-M-0003 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This intake introduces no Lean declaration, so a kernel build would not validate its actual gate.
The smallest real validation is structural and documentary. Exact Lean validation belongs to the
dependent statement phase; master acceptance remains outstanding.
