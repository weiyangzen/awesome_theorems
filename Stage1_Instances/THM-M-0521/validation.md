# Intake validation

Base revision: `e9252b1cfdc99a094324c8a10d260769df2eca15`.

This validation covers manifest membership, dossier consistency, JSON integrity, and a narrow
pinned Lean API probe. Because the repository record does not identify one exact proposition, no
canonical target, expression hash, mutation result, human-source acceptance, or proof is claimed.
The pre-existing shared canonical `.lake` symlink was used read-only and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0521` | exit 0; rank 893, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0521/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0521/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0521/IntakeProbe.lean)` | exit 0; all six pinned API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0521 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source selection and independent
review; canonical statement elaboration, expression fingerprint, and mutation tests; immutable
anchor audit; obligation and discovery freezes; proof; hermetic replay; and release acceptance.
They prevent theorem completion but do not invalidate a truthful `planned` intake.
