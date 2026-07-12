# Intake validation

Base revision: `25617e048a6903787488effc25bc724cd3bdd695`.

Validation is limited to target membership, repository-standard consistency, dossier structure,
scoped intake invariants, and whitespace. The preflight worktree contained the untracked reused
path `Formalizations/Lean/.lake`; it was not modified. No canonical Lean proposition exists yet, so
running an unrelated elaboration would not validate this target and no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0565` | exit 0; rank 613, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0565/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0565/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| scoped untracked-file whitespace check using `git diff --no-index --check` | exit 0; no diagnostics |

Known downstream failures: a unique source proposition, exact primary-source anchor, canonical Lean
elaboration and fingerprint, mutation tests, formal-anchor audit, obligation registry, proof,
hermetic replay, and independent review remain open. They prevent theorem completion but do not
invalidate this fail-closed planned intake.
