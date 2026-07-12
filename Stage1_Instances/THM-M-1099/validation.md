# Intake validation

Base revision: `23465358b632677fd22bc17941cba30db19d8176`.

Validation is limited to manifest consistency, dossier structure, scoped planned-state invariants,
and whitespace. No canonical Lean proposition exists, so no elaboration or kernel-proof result is
claimed. The pre-existing untracked `Formalizations/Lean/.lake` link/artifact was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1099` | exit 0; rank 539, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1099/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1099/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1099` | exit 0; no output |

Known downstream failures are exact primary-source theorem identification and independent review,
canonical Lean statement and elaboration, anchor audit, obligation registry, proof, hermetic replay,
and release validation. They prevent theorem completion but do not invalidate this truthful planned
intake. The first downstream blocker is exact source-statement identity.
