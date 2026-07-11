# Intake validation

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, and
whitespace. No canonical Lean expression is frozen in this phase, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1028` | exit 0; rank 221, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1028/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1028/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1028` | exit 0; no output |

Known downstream failures: primary-source theorem/page and errata inspection, Brownian
version/modification and endpoint conventions, exact Lean elaboration, immutable anchor audit,
proof closure, hermetic replay, and independent review remain open. They prevent theorem completion
but do not invalidate this fail-closed planned intake.
