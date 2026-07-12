# Intake validation

Base revision: `8d9629a48fccb5b722dabcaa962142e5045fafd9`.

Validation is limited to target-manifest consistency, dossier structure, scoped intake invariants,
and whitespace. The exact source proposition is unresolved, so no canonical Lean expression exists
and no elaboration or kernel-proof result is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0671` | exit 0; rank 715, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0671/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0671/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0671` | exit 0; no output |

Known downstream failures are intentionally open: primary-source inspection and independent review,
selection of one exact proposition, canonical Lean elaboration and mutation tests, formal-anchor
audit, obligation registry, proof, hermetic replay, and release validation. They prevent theorem
completion but do not invalidate this truthful planned intake.
