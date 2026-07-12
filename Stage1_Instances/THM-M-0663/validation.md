# Intake validation

Base revision: `8a0364bf7de15487629ea1e22a7aef1acabe372a`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation is limited to target membership,
dossier structure/invariants, whitespace, scoped discovery, and a narrow elaboration probe against
existing pinned artifacts. The probe checks library ingredients only. It is not the statement gate
and establishes no canonical proposition or proof result.

The preflight worktree contains the existing untracked `Formalizations/Lean/.lake` artifact. It was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
performed.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0663` | exit 0; rank 707, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| scoped repository and pinned-mathlib `rg` searches for o-minimality and definable intervals | exit 0; generic order/definability APIs and a legacy assumed slot found, but no o-minimal root declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0663/IntakeProbe.lean` | exit 0; first-order structure, definability, order, interval, monotonicity, and continuity ingredients elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both files are valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0663 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

The repository wording does not yet select a unique theorem. Primary-source inspection and review,
canonical Lean elaboration, checked transports and mutations, formal-candidate audit, obligation
registry, proof, hermetic replay, readable reconstruction, and independent verification remain
open. They prevent audit and theorem completion but do not invalidate a self-tested planned intake.
