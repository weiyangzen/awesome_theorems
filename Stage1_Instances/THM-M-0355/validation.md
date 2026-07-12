# Intake validation

Base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`.

This record covers target membership, dossier structure, intake invariants, and a narrow pinned Lean
API probe. The probe receives no statement or proof credit. The existing canonical `.lake` symlink
and artifacts were reused read-only; no update, fetch, clone, dependency build, or other `.lake`
mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0355` | exit 0; rank 848, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0355/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0355/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0355/IntakeProbe.lean)` | exit 0; all six pinned Schwartz/Fourier/L2/basis API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0355 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0355` | exit 0; no output |

Known downstream failures are intentionally open: primary-source inspection and independent review,
exact convention freeze, canonical target elaboration and mutation tests, anchor audit, obligation
registry and discovery freeze, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
