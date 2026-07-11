# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Validation is limited to target-set consistency, dossier structure, JSON syntax, scoped intake
invariants, and whitespace. No canonical Lean target has been frozen, so no elaboration or kernel
proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard valid, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0002` | exit 0; rank 97, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0002/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0002/task-dag.json` | exit 0 |
| scoped Python assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0002` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page inspection, canonical statement,
Lean elaboration, anchor and provenance audit, proof, hermetic replay, and independent review remain
open. These are expected downstream gates and prevent any theorem-completion claim.
