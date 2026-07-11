# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0184` | 0 | rank 131, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0184/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0184/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n '\b(sorry\|admit\|axiom\|placeholder)\b\|fake result\|"theorem_complete"[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-0184/{README.md,intake.json,scope-map.md,source-statement-crosswalk.md,task-dag.json}` | 1 | expected no-match result; no forbidden proof mechanism or completion claim found |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean declaration was introduced,
so no kernel result is claimed. Exact source identification, statement elaboration, all dependent
phases, node-specific receipt acceptance, and master acceptance remain outstanding.
