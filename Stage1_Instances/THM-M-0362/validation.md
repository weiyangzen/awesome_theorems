# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation covers target membership, dossier
structure, JSON integrity, and a narrow pinned Lean API probe. Since the repository record does not
determine a proposition, no canonical target, expression hash, mutation result, formal anchor, or
proof is claimed.

The preflight worktree contains the existing untracked `Formalizations/Lean/.lake` link/artifact.
It was used read-only. No `lake update`, `lake build`, clone, fetch, or dependency mutation was run.

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
| `python3 scripts/stage1_target.py show THM-M-0362` | exit 0; rank 855, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| bounded `rg` search for Hardy-space and atomic-decomposition names in pinned mathlib analysis sources | exit 0; generic `Lp` material found, no Hardy/atomic-decomposition root located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0362/IntakeProbe.lean` | exit 0; all seven pinned analytic API checks elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0362` | exit 0; no output |

Known downstream open gates are primary-source selection/review, exact statement elaboration and
mutations, obligation and discovery freezes, formal-anchor audit, proof, hermetic replay, readable
reconstruction, and independent release acceptance. They prevent audit and theorem completion but
do not invalidate a truthful `planned` intake.
