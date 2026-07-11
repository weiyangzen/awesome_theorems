# Intake validation

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

Validation is limited to manifest/standard consistency, dossier structure, scoped intake invariants,
JSON syntax, and whitespace. The source phrase names a theory rather than an exact theorem, so no
canonical Lean expression or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1062` | exit 0; rank 505, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1062/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1062/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1062` | exit 0; no output |

Known downstream failures are the exact primary-source theorem selection and inspection, canonical
Lean elaboration, anchor audit, proof architecture and proof, hermetic replay, and independent
review. These prevent theorem completion but do not invalidate this fail-closed planned intake.
