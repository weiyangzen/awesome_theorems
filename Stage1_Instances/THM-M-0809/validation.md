# Intake validation

Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Since the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, or proof is claimed. The existing shared `.lake` artifacts were
used read-only and were not updated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0809` | exit 0; rank 812, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0809/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0809/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0809/IntakeProbe.lean)` | exit 0; all six pinned descriptive-set-theory API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0809` | exit 0; no output |

Known downstream gates remain intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, anchor audit,
proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
