# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). Validation is limited to
manifest consistency, dossier structure, scoped intake invariants, JSON syntax, and whitespace.
There is no canonical Lean expression yet, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1068` | exit 0; rank 510, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1068/instance.json` | exit 0; JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1068/task-dag.json` | exit 0; JSON parsed |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1068 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are deliberate and explicit: pinpoint source inspection and independent
review, exact statement selection, Lean elaboration and mutation tests, formal-candidate audit,
obligation registry, proof, composition, hermetic replay, and independent verification remain open.
They prevent theorem completion but do not invalidate this planned intake.
