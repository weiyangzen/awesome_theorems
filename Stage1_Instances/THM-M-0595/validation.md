# Intake validation record

Base revision: `e92cb303184b333d3c425268001287a1fc3fb3e3`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0595` | 0 | rank 634, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0595/intake.json >/dev/null` | 0 | Structured intake is valid JSON |
| `test -f Stage1_Instances/THM-M-0595/README.md -a -f Stage1_Instances/THM-M-0595/source_statement_crosswalk.md -a -f Stage1_Instances/THM-M-0595/validation.md` | 0 | Required dossier, scope map, crosswalk, and validation record exist |
| `test -z "$(find Stage1_Instances/THM-M-0595 -type f -name '*.lean' -print -quit)"` | 0 | Intake introduces no Lean source, consistent with making no elaboration or kernel claim |
| `rg -n '\\bsorry\\b\\|\\badmit\\b\\|\\bsorryAx\\b\\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0595 --glob '*.lean'` | 1 | No forbidden proof escape occurs in Lean sources; exit 1 is the expected no-match result (and this intake has no Lean source) |
| `git diff --check -- Stage1_Instances/THM-M-0595 .stage1-worker-selftest.json` | 0 | No whitespace errors before self-test manifest creation; rerun below binds the final manifest too |

These are the smallest real checks for this intake-only node. No Lean declaration is introduced,
because the source wording does not yet determine an exact proposition; consequently no kernel
elaboration or proof result is claimed. Exact-statement selection, source closure, all proof and
release gates, and master acceptance remain open.
