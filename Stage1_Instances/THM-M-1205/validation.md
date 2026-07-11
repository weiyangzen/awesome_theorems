# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

Validation is limited to target-set consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean proposition has been selected, so no elaboration or kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1205` | exit 0; rank 170, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1205/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1205/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1205` | exit 0; no output |

Known downstream failures: primary-theorem selection and inspection, exact statement, Lean
elaboration, anchor audit, obligation registry, proof, hermetic replay, and independent review
remain open. They prevent theorem completion but do not invalidate a truthful planned intake.
