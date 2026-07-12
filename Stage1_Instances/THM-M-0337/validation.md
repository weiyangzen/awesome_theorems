# Intake validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`106084d7f6343f3046dfb9e108503edbcdc86191`.

The worktree already contained the unrelated untracked `Formalizations/Lean/.lake` symlink before
this intake. It was neither read as target evidence nor modified. This is worker evidence from a
dirty clone, not release evidence.

## Commands and results

All commands ran from the repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0337` plus `jq` assertions | 0 | Membership, rank 830, `planned`, and `theorem_complete=false` confirmed |
| `jq` closed assertions over `intake.json` | 0 | Schema/item/theorem/lifecycle, null statement, blocker state, two public targets, and noncompletion confirmed |
| `jq` closed assertions over `intake-tasks.json` | 0 | Planned four-task DAG, zero accepted tasks, and noncompletion confirmed |
| dossier-local Python reference and dependency check | 0 | Public merge targets exist; task IDs are unique; every dependency resolves; accepted set is empty |
| `git diff --check` | 0 | No whitespace errors |

The checks were executed as one fail-fast shell validation and printed
`dossier reference and task-DAG checks: ok` after the structural assertions.

## Lean boundary

No `lake env lean` command was run. The intake found no source proposition from which an exact Lean
expression could truthfully be derived. Elaborating a definition or a worker-selected theorem
would not validate the assigned target; it would violate the no-substitution rule. The actionable
retry condition is recorded in `statement-blocker.md`.

These results self-test only `S56-M-0337-INTAKE`. They establish a structurally coherent planned
dossier, scope map, source-statement crosswalk, and open task DAG. They establish no exact
statement, accepted receipt, source proof, kernel proof, audit completion, or theorem completion.
