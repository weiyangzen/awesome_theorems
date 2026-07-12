# Intake validation

Base revision: `3aea47164cf4c9348fbb584dff8a1197a30fca1e`.

Validation is limited to manifest consistency, dossier structure, scoped planned-intake
invariants, JSON syntax, toolchain availability, and whitespace. The source label identifies an
algorithm rather than a proposition, so no canonical Lean expression exists and no elaboration or
kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1103` | exit 0; rank 543, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0 release, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1103/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1103/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1103` | exit 0; no output |

Known downstream failures are exact primary-source theorem selection and independent review,
canonical Lean elaboration and mutation tests, formal-candidate audit, obligation registry, proof,
hermetic replay, and independent release validation. They prevent audit and theorem completion but
do not invalidate this truthful planned intake.
