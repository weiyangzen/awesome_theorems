# Intake validation

Base revision: `3ba2d9fd086e5b49bf2ca5268e302f89ef4a2b03`.

Validation is limited to repository/manifest consistency, dossier structure, pinned toolchain
availability, scoped intake invariants, JSON syntax, and whitespace. There is no canonical Lean
expression in this planned intake, so the Lean version probe is environment evidence only and no
kernel proof or statement elaboration is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1107` | exit 0; rank 547, planned, L0/rework_required, theorem_complete false |
| `lake env lean --version` from `Formalizations/Lean` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-1107/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1107/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1107` | exit 0; no output |

The linked `Formalizations/Lean/.lake` is pre-existing canonical pinned infrastructure and was not
mutated. Known downstream failures are the primary-source pinpoint/normalization audit, canonical
Lean elaboration and mutation tests, anchor audit, obligation registry, proof, hermetic replay, and
independent review. They prevent theorem completion but do not invalidate a fail-closed planned
intake.
