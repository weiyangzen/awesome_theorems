# Intake validation record

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1175` | 0 | rank 375; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1175/intake.json >/dev/null` | 0 | structured intake parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1175/task-dag.json >/dev/null` | 0 | open task DAG parsed |
| `test -f Stage1_Instances/THM-M-1175/README.md -a -f Stage1_Instances/THM-M-1175/source_statement_crosswalk.md` | 0 | dossier and source crosswalk exist |
| `rg -n 'sorry\|axiom\|fake result\|THM-M-0387' Stage1_Instances/THM-M-1175` | 1 | no forbidden proof-device wording, fake-result wording, or copied fixture ID found; exit 1 is `rg`'s no-match result |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It covers manifest consistency and
intake artifact structure only. No Lean theorem exists in this phase, so no kernel result is
claimed. Master acceptance and every dependent phase remain outstanding.
