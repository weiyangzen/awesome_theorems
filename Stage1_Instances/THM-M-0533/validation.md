# Intake validation

Base revision: `8957e7b8e92faa5c99376c8f291502ea568a7271`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean expression exists at intake, so running Lean would
not validate the target and no kernel result is claimed. The existing untracked
`Formalizations/Lean/.lake` link/artifact predates this work and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0533` | exit 0; rank 590, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0533/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0533/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0533` | exit 0; no output |

Known downstream failures: exact source inspection, independent source review, canonical Lean
elaboration, mutation tests, anchor audit, obligation registry, proof, hermetic replay, and
independent validation remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
