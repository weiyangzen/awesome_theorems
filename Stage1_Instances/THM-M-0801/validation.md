# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`5278269d3ea693eba5c4c533ad3fe61693da0620`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
screening, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, source acceptance, or proof is
claimed. The pre-existing canonical `.lake` link/artifacts were used read-only; no update, build,
fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0801` | exit 0; rank 805, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0801/instance.json` | exit 0; syntactically valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0801/task-dag.json` | exit 0; syntactically valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; IDs, lifecycle, root vector, empty accepted states, open ordered DAG, and owned files agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0801/IntakeProbe.lean)` | exit 0; all six pinned cardinal/syntax API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0801 -g '*.lean'` | exit 1, expected no-match; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0801` | exit 0; no output |

Known downstream gates intentionally remain open: exact primary-source selection and independent
review, canonical statement elaboration and mutation tests, obligation and discovery freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
