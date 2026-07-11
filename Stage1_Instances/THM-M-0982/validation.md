# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. This phase does not select or kernel-check a canonical Lean target.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0982` | exit 0; rank 262, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0982/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0982/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0982` | exit 0; no output |

Known downstream failures are the pinpoint primary-source audit, canonical elaboration and mutation
tests, anchor/provenance audit, obligation freeze, proof, hermetic replay, and independent review.
They prevent theorem completion but do not invalidate a fail-closed planned intake.
