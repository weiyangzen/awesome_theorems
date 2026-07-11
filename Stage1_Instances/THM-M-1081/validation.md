# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Validation is limited to target/standard consistency, dossier structure, fail-closed intake
invariants, JSON syntax, and whitespace. Source identity remains ambiguous and there is no
canonical Lean expression, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1081` | exit 0; rank 523, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1081/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1081/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1081 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: primary theorem pinpoint and source-variant resolution, exact Lean
statement/elaboration, mutation checks, anchor audit, obligation registry, proof, hermetic replay,
and independent review remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
