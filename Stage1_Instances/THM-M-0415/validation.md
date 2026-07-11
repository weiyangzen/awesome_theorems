# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

Validation is limited to manifest/standard consistency, dossier structure, and scoped intake
invariants. The legacy Lean file was inspected only as discovery input; no kernel result or proof
credit is claimed in this phase.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0415` | exit 0; rank 70, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0415/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0415/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0415` | exit 0; no output |

Known downstream failures: no primary-source proof edition/page has been accepted; the exact Lean
target has not been elaborated; anchor provenance, proof obligations, kernel replay, hermetic
validation, and independent review are open. These boundaries prevent theorem completion but do
not invalidate a self-tested planned intake.
