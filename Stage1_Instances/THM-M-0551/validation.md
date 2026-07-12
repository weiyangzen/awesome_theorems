# Intake validation

Base revision: `4ded08c944b0cce883dd8b2421be349e11ae9a99`.

Validation is limited to target-set consistency, dossier structure, planned-state invariants, and
whitespace. There is no canonical Lean expression in this intake, so no elaboration or kernel-proof
result is claimed. The existing untracked `Formalizations/Lean/.lake` link/cache was present before
this work and was neither modified nor used as release evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0551` | exit 0; rank 603, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0551/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0551/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0551` | exit 0; no output |

Known downstream failures are the pinpoint primary-source/errata audit, exact space and cohomology
conventions, canonical Lean elaboration, formal-anchor audit, obligation registry, proof,
hermetic replay, and independent review. They prevent audit and theorem completion but do not
invalidate this fail-closed planned intake.
