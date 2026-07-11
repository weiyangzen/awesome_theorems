# Intake validation

Base revision: `2d0ac727836c39cd946970b1ba5903ae1cd8f79d`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression exists, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0460` | exit 0; rank 308, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0460/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0460/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0460` | exit 0; no output |

Known downstream failures: exact primary-source inspection and independent review, canonical Lean
statement and elaboration, anchor audit, obligation registry, proof, hermetic replay, and release
validation remain open. They prevent theorem completion but do not invalidate a truthful planned intake.
