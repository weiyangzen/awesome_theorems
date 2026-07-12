# Intake validation

Base revision: `d555a39d2d8df1572a35ff1b8b14d800b7dae830`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
pinned-environment vocabulary elaboration, and whitespace. The worktree already contained the
untracked canonical `.lake` link/artifact before this task; it was used read-only and was not
created or mutated here. No canonical Lean expression or proof has been selected, so no theorem
kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0318` | exit 0; rank 684, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0318/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0318/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0318/IntakeProbe.lean)` | exit 0; `Set`, `Convex`, `IsCompact`, `ContinuousOn`, and `Set.MapsTo` elaborated under the pinned toolchain |
| `git diff --check -- Stage1_Instances/THM-M-0318` | exit 0; no output |

Known downstream failures: primary-source theorem/page/errata inspection, exact source-form choice,
minimal imports, canonical target elaboration and expression hash, mutation tests, anchor audit,
obligation registry, proof, hermetic replay, and independent review remain open. These prevent
theorem completion but do not invalidate this fail-closed planned intake.
