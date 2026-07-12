# Intake validation

Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. It does not validate a canonical proposition or proof because the source variant is
not yet selected. The pre-existing shared `.lake` link/artifact was used read-only; no dependency
update, fetch, clone, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0341` | exit 0; rank 834, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0341/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0341/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0341/IntakeProbe.lean)` | exit 0; both transform definitions and four pinned inversion declarations elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0341` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, full anchor
audit, proof/provenance classification, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
