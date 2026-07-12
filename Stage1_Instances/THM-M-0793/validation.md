# Intake validation

Base revision: `1c5adf59c0f8176526cb4c9fb281b3ff340c9eeb`.

This record covers manifest membership, the planned dossier, JSON invariants, and a narrow pinned
Lean API probe. The shared canonical `.lake` artifacts are used read-only. Because the source does
not determine a proposition, the probe establishes only that general encoding ingredients
elaborate; it is not a canonical target, mutation test, or proof.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0793` | exit 0; rank 798, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0793/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0793/task-dag.json` | exit 0 |
| scoped Python dossier assertions | exit 0; identity, planned lifecycle, null claim/target, empty accepted state, open task order, and owned files agree |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0793/IntakeProbe.lean)` | exit 0; ordinal, preorder, partial-order, indexed preorder, finite-support, and countable-support ingredients elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0793 -g '*.lean'` | exit 1 as expected for no matches; no prohibited proof placeholder or axiom occurs |
| `git diff --check -- Stage1_Instances/THM-M-0793 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

Known downstream open gates are source selection and independent review, exact statement
elaboration and mutation tests, obligation/discovery freezes, anchor audit, proof, hermetic
validation, and master release. They do not invalidate this truthful `planned` intake.
