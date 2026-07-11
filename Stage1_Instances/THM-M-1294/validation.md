# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No canonical Lean expression exists at intake, so no
elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1294` | exit 0; rank 174, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1294/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1294/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1294` | exit 0; no output |

Known downstream failures: primary-source selection and inspection, theorem/page and errata
verification, canonical Lean elaboration, anchor audit, proof, hermetic replay, and independent
review remain open. They prevent theorem completion but do not invalidate this fail-closed intake.
