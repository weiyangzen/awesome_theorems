# Intake validation

Base revision: `ef32fd7c384b998c2d1505d21d9b5ea7940310b9`.

Validation is intentionally limited to manifest consistency, planned-state dossier invariants,
JSON syntax, and whitespace. Intake has not produced a canonical Lean expression, so this record
does not claim target elaboration, kernel proof evidence, source acceptance, audit completion, or
theorem completion. The pre-existing untracked `Formalizations/Lean/.lake` symlink points to the
canonical pinned artifacts and makes the worktree evidence nonrelease; it was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0172` | exit 0; rank 667, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0172/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0172/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0172` | exit 0; no output |

Environment identity: `Formalizations/Lean/lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`Formalizations/Lean/lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Known downstream failures are the source formula and errata review, exact Lean statement and
mutation suite, immutable candidate audit, frozen obligation registry and typed graphs, proof,
hermetic validation, and release review. They prevent audit and theorem completion but do not
invalidate this fail-closed `planned` intake.
