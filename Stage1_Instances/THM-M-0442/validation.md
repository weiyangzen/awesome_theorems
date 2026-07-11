# Intake validation record

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | rank 88; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0442/instance.json >/dev/null` | 0 | structured instance is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0442/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0442` | 1 | no prohibited Lean declaration tokens found; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0442 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for a documentation-and-structured-data intake. It checks
target-set consistency, membership, JSON syntax, prohibited proof declarations, and whitespace.
No Lean declaration was created or accepted, so these results provide no kernel-proof evidence.
Master acceptance and every dependent phase remain open.
