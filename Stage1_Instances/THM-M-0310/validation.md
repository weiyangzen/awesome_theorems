# Intake validation

Base revision: `fd6e96d8970d08508a2a47d4d6e47e30eeb80164`.

Validation is limited to target-set consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, and whitespace. No canonical Lean expression has been selected,
so no elaboration or kernel-proof result is claimed. Existing `.lake` artifacts were used read
only; no update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0310` | exit 0; rank 680, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0310/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0310/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0310 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical
Lean elaboration and mutation tests, formal-anchor audit, obligation registry, proof, hermetic
replay, and release validation. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
