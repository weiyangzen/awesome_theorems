# Intake validation

Base revision: `6fb5d7698be077f0e9c0e01fac425d492ec114c8`.

Validation date: 2026-07-12 (Asia/Shanghai). Validation is limited to manifest consistency,
dossier structure, scoped intake invariants, and a discovery-only elaboration probe against the
existing pinned environment. The source does not determine a canonical proposition, so no exact
statement or proof result is claimed.

The preflight worktree contains the pre-existing untracked `Formalizations/Lean/.lake`
link/artifact. It was used read-only. No `lake update`, `lake build`, clone, fetch, or dependency
mutation was performed.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0680` | exit 0; rank 721, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0680/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0680/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0680/IntakeProbe.lean` | exit 0; all five discovery-only differential-algebra vocabulary checks elaborated |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0680 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

Primary-source selection, exact statement identity, alternate transports, formal-candidate audit,
obligation registry, proof, trust closure, readable reconstruction, hermetic replay, and independent
verification remain open. They prevent audit and theorem completion but do not invalidate a
truthful planned intake.
