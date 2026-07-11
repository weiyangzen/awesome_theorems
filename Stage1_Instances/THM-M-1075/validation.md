# Intake validation

Base revision: `65062914df38e17a7b33d43f303feb92974e31b5`.

Validation is limited to target-set consistency, planned-dossier structure, scoped intake
invariants, JSON syntax, and whitespace. There is no canonical Lean proposition, so no Lean
elaboration or kernel proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1075` | exit 0; rank 517, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1075/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1075/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1075 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact theorem recovery and primary-source inspection, canonical Lean
elaboration, formal-anchor audit, obligation registry, proof, hermetic replay, and independent
review. They prevent theorem completion but do not invalidate this truthful planned intake.
