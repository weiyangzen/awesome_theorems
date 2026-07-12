# Intake validation

Base revision: `bd0d227173ac95971603f633607751754850337e`.

Validation covers target-manifest consistency, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. Because no canonical Lean target has been frozen,
the probe is not a statement elaboration, expression fingerprint, mutation test, or proof. The
existing canonical `.lake` artifacts were used read-only and were not updated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0346` | exit 0; rank 839, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0346/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0346/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0346/IntakeProbe.lean)` | exit 0 after correcting the probe's unqualified Haar-measure name; all eight pinned APIs elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0346` | exit 0; no output |

Known downstream failures are intentionally open: pinpoint primary-source inspection and independent
review, canonical statement elaboration and mutation tests, discovery and obligation freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion
but do not invalidate a truthful `planned` intake.
