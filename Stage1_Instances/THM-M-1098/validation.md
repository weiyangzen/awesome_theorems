# Intake validation

Base revision: `23465358b632677fd22bc17941cba30db19d8176` (commit timestamp
`2026-07-12T12:13:31+08:00`).

Validation is limited to manifest consistency, dossier structure, planned-intake invariants, JSON
syntax, and whitespace. The source wording does not identify one proposition and no canonical Lean
expression exists, so running `lake env lean` would not test this intake and no elaboration or
kernel-proof result is claimed. The pre-existing untracked `Formalizations/Lean/.lake` link/artifact
was not created or modified by this task.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1098` | exit 0; rank 538, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1098/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1098/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1098` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical Lean
elaboration and mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent release validation. They prevent audit and theorem completion but do not invalidate
this truthful planned intake.
