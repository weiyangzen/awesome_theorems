# Intake validation

Base revision: `3320329db47d2d9804ae3322159af1f5125bbcf7`.

Validation is limited to repository/manifest consistency, dossier JSON syntax, scoped intake
invariants, and whitespace. There is no canonical Lean expression in the intake phase, so running
`lake env lean` would not test this theorem and no kernel result is claimed. The pre-existing
untracked `Formalizations/Lean/.lake` path was not created or modified here; this is nonrelease
worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0192` | exit 0; rank 678, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0192/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0192/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0192` | exit 0; no output |

Known downstream failures are exact source transcription and errata review, precise domain and
Frobenius conventions, canonical Lean elaboration and mutation tests, anchor discovery, obligation
registry, proof, hermetic replay, and independent review. These prevent theorem completion but do
not invalidate a fail-closed planned intake.
