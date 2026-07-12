# Intake validation

Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Since the repository record contains no proposition, no canonical target,
expression hash, mutation result, arithmetic-circuit model, or proof is claimed. The canonical
`.lake` artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0734` | exit 0; rank 771, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -i 'THM-M-0734|代数复杂性|代数计算复杂性' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Blueprint_Applicable_Theorems.md` | exit 0; only the topic gloss and open Stage0 fields identify this target |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0734/IntakeProbe.lean)` | exit 0; six pinned multivariate-polynomial API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0734 -g '*.lean'` | exit 1, expected no-match; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0734/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0734/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0734` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source selection and independent
review, canonical statement elaboration and mutation tests, obligation/discovery freezes, formal-
anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but
do not invalidate a truthful `planned` intake.
