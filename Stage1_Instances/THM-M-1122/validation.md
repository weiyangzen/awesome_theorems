# Intake validation

Base revision: `646931af665a6683a1fa53db71b5416bee63abff`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, and whitespace. No canonical Lean expression has been selected,
so no elaboration or kernel-proof result is claimed. No `.lake` content was fetched or mutated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1122` | exit 0; rank 562, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1122/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1122/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1122 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical
Lean elaboration and mutation tests, formal-anchor audit, obligation registry, proof, hermetic
replay, and release validation. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
