# Intake validation

Base revision: `e51894725a43642d26ce16e4aad3abaf28393de7`.

Validation is limited to repository/manifest consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. No canonical Lean expression exists in this phase, so `lake env lean`
would have no exact target to elaborate and no kernel result is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not created or modified by this intake and makes this
nonrelease evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0191` | exit 0; rank 677, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0191/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0191/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0191` | exit 0; no output |

Known downstream failures: pinpoint primary-source statement and errata review, exact domain and
normalization choices, canonical Lean elaboration, mutation tests, discovery protocol, obligation
registry, anchor audit, proof, hermetic replay, and independent review remain open. They prevent
theorem completion but do not invalidate this fail-closed planned intake.
