# Intake validation record

Base revision: `0a66013e1558a3bc4e31c9d7f64c0e8fb1dfebab`.

Validation is scoped to target membership, the planned dossier, its fail-closed boundaries, and the
open dependent-task chain. There is no exact Lean proposition at intake, so no kernel elaboration or
proof result is claimed. The existing canonical `.lake` artifacts were not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0179` | 0 | Rank 670, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0179/intake.json` | 0 | Structured intake is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0179/task-dag.json` | 0 | Open task DAG is valid JSON |
| scoped Python intake assertions | 0 | IDs, lifecycle, empty accepted states, status boundary, file set, and linear open dependencies passed |
| `git diff --check -- Stage1_Instances/THM-M-0179` | 0 | No whitespace errors |

Known downstream failures are the missing immutable primary-source theorem locator, unresolved exact
claim, canonical Lean elaboration, formal-candidate audit, obligation registry and typed graphs,
proof, hermetic replay, and independent review. They keep the root at provisional `[H1, M4, R3]`
and prevent audit or theorem completion, but do not invalidate this intentionally planned intake.
