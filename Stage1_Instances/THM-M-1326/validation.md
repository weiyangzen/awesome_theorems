# Intake validation

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. There is no frozen Lean expression, so this intake records no kernel result.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1326` | exit 0; rank 488, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1326/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1326/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1326` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page inspection, curvature and Laplacian
normalizations, cut-locus semantics, canonical Lean elaboration, immutable anchor audit, proof,
hermetic replay, and independent review remain open. They do not invalidate a fail-closed planned
intake, but they prevent any theorem-completion claim.
