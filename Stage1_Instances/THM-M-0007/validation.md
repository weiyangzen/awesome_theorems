# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Validation covers manifest/standard consistency, dossier syntax and scoped intake invariants. No
exact Lean target has been frozen, so no kernel closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0007` | exit 0; rank 94, L0/rework required, planned, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0007/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0007/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0007` | exit 0; no output |

Known downstream failures: the primary text has not received page-level transcription and errata
review; typed spectral-sequence naturality and convergence are not elaborated; proof, hermetic
replay, and independent acceptance remain open. These do not invalidate a fail-closed intake.
