# Intake validation

Base revision: `65f25d08d2043f95837c8686cce016cee3fe3d0e` (tree
`fc689bbba422127736141993537f94b672008375`).

Validation is limited to target membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, pinned toolchain availability, and whitespace. Intake has no
canonical Lean expression, so running `lake env lean` on an invented theorem would be invalid and
no kernel theorem-proof result is claimed. The automation-provided `Formalizations/Lean/.lake`
symlink is untracked and points at the canonical pinned artifacts; it was neither created nor
mutated by this run and makes the evidence nonrelease worktree evidence.

| Command (from repository root unless noted) | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0588` | exit 0; rank 628, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0588/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0588/task-dag.json` | exit 0 |
| scoped Python assertions over instance identity, lifecycle, rank, accepted states, formal target, and six open downstream nodes | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-0588` | exit 0; no output |

An initial toolchain probe was mistakenly run from the repository root, where there is no
`lean-toolchain`; it exited nonzero with "no default toolchain configured." Repeating the required
command from the pinned Lean project directory succeeded as recorded above. No dependency update,
build, clone, fetch, or `.lake` mutation was performed.

Known downstream failures are intentionally open: exact primary-source theorem/page and attribution
review, canonical Lean target elaboration and mutation tests, immutable anchor audit, obligation
registry, proof, hermetic replay, and independent release verification. They prevent audit and
theorem completion but do not invalidate this fail-closed planned intake.
