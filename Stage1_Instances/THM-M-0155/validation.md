# Intake validation

Base revision: `48f7c2e56c585d0c605516ac55e10ac7b5e1679d`.

Validation is limited to target membership, standard consistency, dossier structure, scoped intake
invariants, and whitespace. The pre-existing untracked `Formalizations/Lean/.lake` symlink is the
canonical pinned artifact reuse described by the worker environment; it was not modified. No exact
Lean target exists in this intake, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0155` | exit 0; rank 654, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0155/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0155/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0155` | exit 0; no output |

Known downstream failures: exact primary-source theorem/page inspection, independent source review,
canonical Lean statement and environment fingerprint, mutation tests, formal-candidate audit,
obligation registry, proof, hermetic replay, and independent release verification remain open. They
prevent theorem completion but do not invalidate this truthful planned intake.
