# Intake validation

Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`.

This validation covers target membership, dossier structure, JSON integrity, source-record
inspection, and a narrow pinned Lean API probe. Because the source does not identify a proposition,
no canonical target, expression hash, mutation result, or proof is claimed. The pre-existing
canonical `.lake` artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0794` | exit 0; rank 799, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 12 'THM-M-0794|适当力迫|保持基数的力迫' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; only topic/gloss metadata and open Stage0 fields found |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0794/IntakeProbe.lean)` | exit 0; all eight nearby pinned order/cardinal APIs elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0794/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0794/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0794 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0794` | exit 0; no output |

Known downstream failures are intentionally open: immutable source selection and independent
review, canonical statement elaboration and mutation tests, obligation and discovery freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
