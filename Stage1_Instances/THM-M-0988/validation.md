# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The legacy Lean artifact was inspected only as discovery input; this
phase does not claim a fresh canonical elaboration or kernel proof.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0988` | exit 0; rank 268, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0988/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0988/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0988` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page and errata inspection, canonical
statement fingerprint, anchor and axiom audit, frozen obligation graphs, proof acceptance,
hermetic replay, and independent review remain open. These prevent theorem completion without
invalidating a fail-closed planned intake.
