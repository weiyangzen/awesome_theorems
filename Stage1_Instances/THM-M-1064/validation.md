# Intake validation

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

Validation is intentionally limited to manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean target has been selected, so no elaboration or kernel
proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1064` | exit 0; rank 220, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1064/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1064/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1064` | exit 0; no output |

Known downstream failures are source-variant disambiguation, exact theorem/page and errata review,
canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic replay, and
independent review. They prevent theorem completion but do not invalidate this fail-closed intake.
