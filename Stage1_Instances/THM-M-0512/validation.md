# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify an exact formula, no canonical
target, expression hash, mutation result, or proof is claimed. The pre-existing canonical `.lake`
link/artifacts were used read-only; no dependency update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0512` | exit 0; rank 886, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0512/instance.json` | exit 0; JSON valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0512/task-dag.json` | exit 0; JSON valid |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0512/IntakeProbe.lean)` | exit 0; all five pinned API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0512 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom in Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0512` | exit 0; no output |

Known downstream failures are intentionally open: immutable source selection and independent
review, canonical statement elaboration and mutation tests, obligation and discovery freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
