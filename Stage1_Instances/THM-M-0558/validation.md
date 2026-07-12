# Intake validation

Base revision: `c8997e79129038d11a59ae2ad24c3725dcc2d8b9`.

Validation is scoped to manifest membership, planned-instance structure, the pinned Lean executable,
and intake invariants. No canonical Lean expression exists yet, so the Lean version check is not an
elaboration or kernel-proof claim. The pre-existing untracked `Formalizations/Lean/.lake` link is
classified as unrelated worker-clone state; it was inspected but not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0558` | exit 0; rank 606, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0558/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0558/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0558` | exit 0; no output |

Known downstream failures are exact primary-source/errata review, a canonical Lean expression and
mutation tests, formal-anchor audit, obligation registry, proof, hermetic validation, and independent
review. They prevent audit and theorem completion but do not invalidate a fail-closed planned intake.
