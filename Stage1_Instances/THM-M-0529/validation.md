# Intake validation

Base revision: `54912addae847c8bb166d0ef6a8ec7b0abb53004`.

Validation is limited to target membership, repository-standard consistency, dossier structure,
planned-state invariants, and whitespace. The exact source theorem and canonical Lean expression
remain open, so this intake makes no elaboration or kernel-proof claim. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not created or modified by this intake and makes this
a nonrelease workspace.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0529` | exit 0; rank 586, no legacy slot, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0529/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0529/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0529` | exit 0; no output |

Known downstream failures are exact primary-source selection and inspection, source review,
canonical Lean elaboration and mutation tests, formal-anchor audit, obligation freeze, proof,
hermetic replay, and independent verification. They prevent audit and theorem completion but do not
invalidate a fail-closed `planned` intake.
