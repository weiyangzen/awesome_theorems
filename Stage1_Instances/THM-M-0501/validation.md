# Intake validation

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify an exact proposition, no canonical
target, expression hash, mutation result, or proof is claimed. The pre-existing shared canonical
`.lake` artifacts were used read-only; no dependency mutation command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0501` | exit 0; rank 878, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0501/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0501/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0501/IntakeProbe.lean)` | exit 0; all six pinned analytic-number-theory API checks elaborated under Lean 4.29.0 |
| per-file `git diff --no-index --check -- /dev/null <owned-file>` loop | expected exit 1 for each untracked addition with empty diagnostics; `untracked diff check: ok` |

Known downstream failures are intentionally open: primary source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
