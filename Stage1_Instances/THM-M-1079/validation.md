# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). Validation is limited to
target membership, standard consistency, dossier JSON and scoped intake invariants, and whitespace.
There is no canonical Lean expression, so no elaboration or kernel result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1079/instance.json >/dev/null` | 0 | JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1079/task-dag.json >/dev/null` | 0 | JSON parsed |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1079` | 0 | rank 521, planned, L0/rework_required, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1079 .stage1-worker-selftest.json` | 0 | no output |

Known downstream failures are explicit: exact source-property selection, canonical Lean
elaboration, source and formal-anchor audits, obligation freezing, proof, hermetic replay, and
independent review remain open. They prevent theorem completion but do not invalidate a fail-closed
planned intake.
