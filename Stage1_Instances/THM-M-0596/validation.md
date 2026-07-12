# Intake validation

Base revision: `e92cb303184b333d3c425268001287a1fc3fb3e3`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, pinned
toolchain availability, and whitespace. There is deliberately no `.lean` target at intake: the
repository phrase does not determine an exact proposition, so elaborating a chosen variant would
broaden or substitute the theorem. Consequently, the Lean version check below is environment
evidence, not statement or kernel-proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0596` | exit 0; rank 635, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0596/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0596/task-dag.json` | exit 0 |
| scoped Python intake assertions and prohibited-token scan | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0596` | exit 0; no output |

Known downstream failures are exact source theorem/page and assumption inspection, canonical Lean
elaboration and mutation tests, immutable anchor audit, obligation freeze, proof, hermetic replay,
and independent review. They prevent audit and theorem completion but do not invalidate this
fail-closed planned intake.
