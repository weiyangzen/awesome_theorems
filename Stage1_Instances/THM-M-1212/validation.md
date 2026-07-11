# Intake validation

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, JSON syntax, and whitespace. No Lean declaration is introduced, so no elaboration or
kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1212` | exit 0; rank 405, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1212/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1212/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| scoped forbidden proof-token scan | exit 0; no matches |
| `git diff --check -- Stage1_Instances/THM-M-1212` | exit 0; no output |

Known downstream failures: exact primary-source selection and inspection, theorem/page and errata
verification, canonical Lean elaboration, anchor audit, obligation expansion, proof, hermetic replay,
and independent review remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake. Master acceptance is also outstanding.
