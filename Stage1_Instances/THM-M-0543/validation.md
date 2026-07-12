# Intake validation

Base revision: `ed3ed0f054485ec0127b6322b75cd061be59d105`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, repo-local source discovery, and whitespace. No canonical Lean expression has been
selected, so running `lake env lean` would elaborate a substituted target rather than this theorem;
no kernel result is claimed at intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0543` | exit 0; rank 600, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'de.?rham\\|derham\\|de Rham' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean` | exit 0; local infrastructure/audit hits, but no concrete accepted terminal theorem identified |
| `python3 -m json.tool Stage1_Instances/THM-M-0543/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0543/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0543` | exit 0; no output |

Known downstream failures are exact primary-source inspection and independent review, a canonical
Lean statement and expression fingerprint, mutation tests, immutable anchor audit, obligation
registry, proof, hermetic replay, and independent release validation. They prevent theorem
completion but do not invalidate this truthful planned intake.
