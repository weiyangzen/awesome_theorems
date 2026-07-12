# Intake validation

Base revision: `82592a2cd69e194c41c57127bd211a94db5f3db4`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The worktree already contained the untracked shared
`Formalizations/Lean/.lake` link; it was not modified. No canonical Lean expression has been
selected, so a Lean elaboration command would validate a substituted statement and no kernel result
is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0604` | exit 0; rank 642, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0604/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0604/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0604` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page inspection, selection of the bordism
variant, source review, canonical Lean elaboration and mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and independent validation remain open. They prevent audit and
theorem completion but do not invalidate this fail-closed planned intake.
