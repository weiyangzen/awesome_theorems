# Intake validation

Validation is structural and intake-scoped. No Lean declaration was added, so
no kernel closure is tested or claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 1546 uniform-L0 targets and assurance structure accepted |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0554` | exit 0; rank 106, `planned`, `L0`, rework required |
| `python3 -m json.tool Stage1_Instances/THM-M-0554/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0554/task-dag.json` | exit 0 |
| scoped intake invariant check | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0554` | exit 0 |

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

The first downstream failed gate is the exact Lean statement gate: the bundled
generalized-cohomology and finite-CW interfaces, canonical expression, imports,
environment fingerprint, and mutation tests have not yet been established.
