# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API/proposition probe. It does not claim an exact frozen target or a proof. The pre-existing
shared canonical `.lake` link/artifact was used read-only and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard valid, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0769` | exit 0; rank 779, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0769/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0769/task-dag.json` | exit 0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0769/IntakeProbe.lean)` | exit 0; `Classical.choice`, `Classical.axiomOfChoice`, and the candidate dependent-family proposition elaborated under Lean 4.29.0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0769` | exit 0; no output |

Known downstream failures intentionally remain: primary-passage review, exact target freeze and
mutation tests, anchor and obligation freezes, axiom/provenance audit, proof-state classification,
hermetic validation, and release acceptance. They prevent theorem completion but not a truthful
`planned` intake.
