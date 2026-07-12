# Intake validation

Base revision: `65f25d08d2043f95837c8686cce016cee3fe3d0e`.

Validation is limited to target membership, dossier structure, scoped intake invariants, JSON
syntax, pinned-environment availability, and whitespace. No canonical Lean expression exists, so
running `lake env lean` on an invented declaration would not validate an intake claim. The existing
toolchain and pinned mathlib revision were inspected without modifying `.lake`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0587` | exit 0; rank 627, L0/rework_required, planned, theorem_complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0587/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0587/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0587` | exit 0; no output |

Known downstream failures: stable primary-source scan and pinpoint, errata review, exact dimension
and boundary conventions, canonical Lean elaboration and mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and independent review remain open. They block theorem completion
but do not invalidate this fail-closed planned intake.
