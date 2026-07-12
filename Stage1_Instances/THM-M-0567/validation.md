# Intake validation

Base revision: `2534080bb6434bc903d482fcebdf9e0a05b94398`.

Validation is limited to target membership, repository-standard consistency, dossier structure,
scoped intake invariants, and whitespace. The preflight worktree contained the untracked reused
path `Formalizations/Lean/.lake`; it was not modified. There is no exact canonical Lean proposition
at intake, so an unrelated elaboration would not validate this target and no kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0567` | exit 0; rank 615, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0567/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0567/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| scoped untracked-file whitespace check using `git diff --no-index --check` | exit 0; no diagnostics |

Known downstream failures are intentional and explicit: unique source proposition, primary-source
pinpoint, canonical Lean elaboration and fingerprint, mutation tests, formal-anchor audit,
obligation registry, proof, hermetic replay, and independent review remain open. They prevent audit
and theorem completion but do not invalidate a fail-closed planned intake.
