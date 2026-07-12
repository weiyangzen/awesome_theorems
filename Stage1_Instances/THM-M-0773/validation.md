# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`3159849a5319960dea505779c7c20894ea30487c`.

This validation covers target membership, planned-dossier structure, JSON integrity, and a narrow
pinned Lean API/boundary probe. The pre-existing canonical `.lake` symlink and artifacts were used
read-only. No update, build, clone, fetch, or dependency mutation was run. The worktree already
reported `Formalizations/Lean/.lake` as untracked because the worker clone points at that shared
canonical artifact; this makes the run nonrelease evidence and is not a change owned by this item.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0773` | 0 | rank 781; planned; legacy artifacts unaccepted; theorem_complete false |
| `git rev-parse HEAD` | 0 | `3159849a5319960dea505779c7c20894ea30487c` |
| `git status --short` (pre-edit) | 0 | only pre-existing untracked `Formalizations/Lean/.lake` reported |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0773/IntakeProbe.lean)` | 0 | candidate definition and theorem types printed; empty-family boundary theorem elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0773/instance.json` | 0 | intake manifest is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0773/task-dag.json` | 0 | open task DAG is valid JSON |
| scoped Python intake assertions | 0 | printed `intake invariant check: ok`; checked planned lifecycle, no accepted state, exact target identity, rank, and downstream dependency chain |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0773 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0773` | 0 | no output |

During authoring, the Lean probe was run twice with an unresolved overloaded spelling of the empty
set; both runs exited 1 at `IntakeProbe.lean`. Replacing it with the explicitly type-annotated
`(∅ : Set alpha)` resolved the elaboration error;
the final command above is the validation result and exits 0.

The intake does not claim exact expression hashing, checked alternate transports, statement
mutations, source acceptance, anchor-audit acceptance, proof closure, hermetic replay, or release.
Those remain dependency-ordered open tasks and keep `audit_complete` and `theorem_complete` false.
