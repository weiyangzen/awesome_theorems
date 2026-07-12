# Intake validation

Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`.

Validation is limited to target-set consistency, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. Since the repository record does not select a
unique proposition, no canonical expression, mutation test, or proof result is claimed. The shared
canonical `.lake` link/artifacts were used read only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0327` | exit 0; rank 821, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0327/IntakeProbe.lean)` | exit 0; all six weak-topology, compactness, `L^p`, and uniform-integrability API checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0327/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0327/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0327 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0327 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical
Lean statement elaboration and mutation tests, formal-anchor audit, obligation freeze, proof,
hermetic replay, and release validation. They prevent theorem completion but do not invalidate a
truthful `planned` intake.
