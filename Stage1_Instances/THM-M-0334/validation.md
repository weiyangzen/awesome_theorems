# Intake validation

Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one proposition, no canonical
target, expression hash, statement mutation result, or proof is claimed. The pre-existing canonical
`.lake` artifacts were used read-only; no dependency update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0334` | exit 0 during preflight; rank 827, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0334/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0334/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0334/IntakeProbe.lean)` | exit 0; all six pinned operator-algebra API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0334 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0334` | exit 0; no output |

Known downstream gates intentionally remain open: immutable source pinpoint and independent review,
exact statement selection and elaboration, mutation tests, obligation/discovery freezes, exhaustive
formal-anchor audit, proof, hermetic replay, and release acceptance. These prevent theorem
completion but do not invalidate a truthful `planned` intake.
