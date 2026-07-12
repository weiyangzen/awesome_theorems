# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one exact proposition, no canonical
target, expression hash, transport, mutation result, or proof is claimed. The canonical `.lake`
artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0315` | exit 0; rank 817, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0315/IntakeProbe.lean)` | exit 0; five pinned compact-operator, Fredholm-alternative, spectrum, and bijectivity APIs elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0315/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0315/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0315 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0315` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, complete
formal-anchor audit, proof reconciliation, hermetic replay, and release acceptance. They prevent
theorem completion but do not invalidate a truthful `planned` intake.
