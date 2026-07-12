# Intake validation

Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`.

This validation covers target membership, structured intake consistency, and a narrow probe of the
pinned Lean APIs needed at the statement boundary. It does not claim an elaborated canonical target
or a proof. The pre-existing untracked `Formalizations/Lean/.lake` link is shared automation state;
it was used read-only and no dependency update, fetch, clone, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0518` | exit 0; rank 891, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0518/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0518/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0518/IntakeProbe.lean)` | exit 0; all nine pinned API checks and the local semistability ingredient elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0518` | exit 0; no output |

Known downstream failures are intentionally open: primary-source definition/errata review, exact
global semistability and modularity encodings, statement elaboration and mutation tests, formal
anchor audit, obligation and discovery freezes, proof, hermetic replay, independent validation, and
master acceptance. They prevent theorem completion but do not invalidate a truthful planned intake.
