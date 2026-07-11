# Intake validation

Base revision: `ef0dd4cd5367b81a98b8906e3325b55fe5263491`.

Validation is limited to manifest consistency, JSON syntax, scoped intake invariants, and whitespace.
There is no canonical Lean expression at intake, so no elaboration or kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1295` | exit 0; rank 463, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1295/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1295/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1295` | exit 0; no output |

The exact-source selection, canonical Lean statement, anchor audit, proof, replay, and independent
review remain open downstream gates. This is consistent with a fail-closed `planned` intake.
