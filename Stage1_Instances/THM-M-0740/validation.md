# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a unique quantified proposition,
no canonical target, expression hash, mutation result, or proof is claimed. The existing canonical
`.lake` artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0740` | exit 0; rank 776, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0740/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0740/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0740/IntakeProbe.lean)` | exit 0; all six pinned graph/clique/order API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0740` | exit 0; no output |

Known downstream failures are intentionally open: primary-source inspection and independent
review, exact circuit/function/parameter freeze, circuit interface construction or discovery,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal
anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but
do not invalidate a truthful `planned` intake.
