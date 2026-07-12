# Intake validation

Base revision: `c9694802ae049af37973e49a65f11b833135333f`.

Validation is limited to manifest consistency, dossier structure, JSON integrity, and a narrow
pinned Lean API probe. Because the repository record does not determine an exact proposition, no
canonical target, expression hash, mutation result, source acceptance, or proof is claimed. The
canonical pinned `.lake` artifacts were used read-only and were not updated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0350` | exit 0; rank 843, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0350/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0350/task-dag.json` | exit 0 |
| scoped Python assertions over instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0350/IntakeProbe.lean)` | exit 0; all six pinned analysis API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0350 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source inspection and independent
review, canonical statement elaboration and mutation tests, obligation/discovery freezes, formal
anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but
do not invalidate a truthful `planned` intake.
