# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to target membership, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression at this phase, so no elaboration,
axiom report, placeholder scan of a proof body, or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1070/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1070/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1070` | exit 0; rank 512, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1070 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source inspection, canonical Lean elaboration and mutation
tests, formal-candidate audit, obligation registry, proof, hermetic replay, and independent review
remain open. They prevent audit and theorem completion but do not invalidate this fail-closed
planned intake.
