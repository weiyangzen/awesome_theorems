# Intake validation

Base revision: `65062914df38e17a7b33d43f303feb92974e31b5`.

Validation is limited to target-set consistency, dossier structure, scoped intake invariants, and
whitespace. This phase adds no Lean declaration, so it makes no kernel claim.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1077` | exit 0; rank 519, L0/rework-required, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1077/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1077/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1077` | exit 0; no output |

Known downstream failures are exact primary-source inspection, canonical Lean elaboration,
mutation tests, anchor audit, obligation freeze, proof, hermetic replay, and independent review.
They prevent theorem completion but do not invalidate a fail-closed planned intake.
