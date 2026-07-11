# Intake validation

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
and whitespace. No canonical Lean expression was selected, so no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1030` | exit 0; rank 223, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1030/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1030/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1030` | exit 0; no output |

Known downstream failures: primary-source statement inspection, canonical Lean elaboration, anchor
audit, obligation registry, proof, hermetic replay, and independent review remain open. They prevent
theorem completion but do not invalidate this fail-closed planned intake.
