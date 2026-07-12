# Intake validation

Base revision: `d0c81540f24ae847c2651a18be7e829b4b280213`.

Validation is limited to target-set consistency, dossier structure, scoped planned-state
invariants, JSON syntax, and whitespace. No canonical Lean expression exists at intake, so no
kernel elaboration or theorem-proof result is claimed. The pre-existing untracked
`Formalizations/Lean/.lake` link points to the canonical pinned artifacts, is outside this target's
owned path, and makes this nonrelease worktree evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0582` | exit 0; rank 624, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0582/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0582/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0582` | exit 0; no output |

Known downstream failures: exact primary-source theorem/section inspection, formulation and errata
crosswalk, independent source review, canonical Lean elaboration and mutation tests,
immutable-revision anchor audit, obligation registry, proof, hermetic replay, and release
verification remain open. They prevent audit and theorem completion but do not invalidate a
fail-closed `planned` intake.
