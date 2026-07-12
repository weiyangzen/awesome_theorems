# Intake validation

Base revision: `83c1cc0af3ba7bd4612988241849d2949fad9e72`.

Validation is limited to target/standard consistency, dossier structure, scoped intake invariants,
and whitespace. No canonical Lean expression has been selected, so no elaboration or kernel-proof
result is claimed. The pre-existing untracked `Formalizations/Lean/.lake` link/artifact was not
modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0602` | exit 0; rank 640, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0602/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0602/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0602` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source inspection and independent
review, canonical Lean statement and elaboration, anchor audit, obligation registry, proof,
hermetic replay, and independent release validation. They prevent theorem completion but do not
invalidate a truthful planned intake.
