# Intake validation record

Base revision: `6d9732600c7da75d9b55873adc3303cf64bd77f2`.

All commands ran from the repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0127` | 0 | rank 330; planned; L0/rework-required; untrusted source status; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0127/intake.json >/dev/null` | 0 | intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0127/task-dag.json >/dev/null` | 0 | open task DAG is valid JSON |
| `test -f` for `README.md`, `scope-map.md`, and `source-statement-crosswalk.md` | 0 | required dossier, scope map, and crosswalk exist |
| scoped forbidden-marker no-match assertion | 0 | no Lean escape markers occur in the owned artifacts |
| `git diff --check -- Stage1_Instances/THM-M-0127` | 0 | no whitespace errors |

These checks validate manifest membership and intake artifact structure only. No exact Lean
statement exists to elaborate at this phase, so they provide no kernel-proof or theorem-completion
evidence. Primary-source identification is the recorded blocker for the dependent statement node.
