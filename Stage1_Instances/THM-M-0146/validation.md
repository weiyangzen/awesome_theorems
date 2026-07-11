# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Validation is limited to manifest consistency and dossier structure. No Lean target exists because
the source metadata does not uniquely identify a proposition; consequently no kernel result is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0146` | exit 0; rank 321, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0 for both |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0146` | exit 0; no output |

Known downstream failures are exact source identity and inspection, statement elaboration, anchor
audit, proof, hermetic replay, and independent review. They prevent theorem completion but do not
invalidate this honest planned intake.
