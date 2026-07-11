# Intake validation

Base revision: `65062914df38e17a7b33d43f303feb92974e31b5`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression yet, so no elaboration or kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1078/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1078/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | preflight exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | preflight exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | preflight exit 0; rank 520, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: primary-source pinpoint inspection and independent review, canonical
Lean elaboration, anchor audit, obligation registry, proof, hermetic replay, and release validation
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
