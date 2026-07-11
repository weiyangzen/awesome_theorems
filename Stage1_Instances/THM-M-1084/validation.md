# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression yet, so no elaboration or kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1084/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1084` | exit 0; rank 526, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source inspection, canonical Lean elaboration and mutation
tests, formal-candidate audit, obligation registry, proof, hermetic replay, and independent review
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.

Two development runs of the scoped assertion harness exited 1 because its test code first scanned
documentation for Lean-source tokens and then expected the theorem ID rather than the item-ID stem
inside task IDs. No dossier invariant failed. The final harness scans Lean files only (there are
none at intake), checks task IDs against `S56-M-1084`, and retains all structural assertions.
