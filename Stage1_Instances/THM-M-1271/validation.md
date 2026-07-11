# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean expression exists yet, so no kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1271` | exit 0; rank 164, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1271/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1271/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1271` | exit 0; no output |

Known downstream failures: primary-text inspection, exact Lean elaboration, anchor audit, frozen
obligation graphs, proof, hermetic replay, and independent review remain open. These prevent theorem
completion but do not invalidate a fail-closed planned intake.
