# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

This validation covers manifest membership, dossier structure, JSON integrity, source-record
inspection, and a narrow pinned Lean foundational API probe. Because the repository record does
not assert a proposition, no canonical target, expression hash, statement mutation, or proof is
claimed. The canonical `.lake` symlink and pinned artifacts were used read-only; no update, build,
fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0703` | exit 0; rank 744, planned, legacy artifacts unaccepted, theorem_complete false |
| `sed -n '5190,5195p' Docs/researches/math_theorems.md; sed -n '19214,19237p' Docs/Stage0_Blueprint.md; python3 scripts/stage1_target.py show THM-M-0703` | exit 0; the target-specific records contain only the topic/gloss metadata and open Stage0 fields |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0703/IntakeProbe.lean)` | exit 0; all five foundational API checks elaborated; no canonical theorem asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0703/instance.json` | exit 0; JSON valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0703/task-dag.json` | exit 0; JSON valid |
| scoped Python intake assertions | exit 0; manifest identity, lifecycle, empty accepted states, root vector, and six downstream DAG nodes agree |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0703 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0703` | exit 0; no output |

Known downstream failures remain intentionally open: exact primary-source proposition and
independent review, canonical statement elaboration and mutation tests, obligation/discovery
freezes, anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate this truthful `planned` intake.
