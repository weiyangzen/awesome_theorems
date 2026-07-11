# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

Validation covers repository/manifest consistency, dossier structure, scoped intake invariants,
and whitespace only. No canonical Lean expression exists at this phase, so no elaboration or kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1535` | exit 0; rank 177, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1535/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1535/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1535` | exit 0; no output |

Known downstream failures: exact version-pinned primary-source inspection, a unique mathematical
statement, model foundations, canonical Lean elaboration, anchor audit, proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate a fail-closed
planned intake.
