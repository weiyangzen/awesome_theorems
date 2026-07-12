# Statement validation

Base revision: `f4b142975b0cf41e1c092e006544346545ed8b8c`.

The narrow Lean command elaborates the canonical expression against the existing pinned dependency
artifacts. It does not prove the proposition. No dependency update, build, fetch, or `.lake`
mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1227` | exit 0; rank 416, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1227/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1227/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1227/Statement.lean` | exit 0; `Stage1.THM_M_1227.lerayHopfExistenceTarget : Prop` |
| scoped Python statement assertions (command in worker self-test manifest) | exit 0; `statement invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1227` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page inspection, anchor audit, obligation
expansion, proof, hermetic replay, and independent review remain open. These prevent theorem
completion but do not invalidate the elaborated statement-phase result.
