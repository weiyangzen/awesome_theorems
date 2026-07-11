# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression yet, so no elaboration or kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1082/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1082/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1082` | exit 0; rank 524, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1082 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentional and fail-closed: the source record does not specify a
unique proposition; pinpoint source review, exact Lean elaboration, anchor audit, obligation
registry, proof, hermetic replay, and independent review remain open. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
