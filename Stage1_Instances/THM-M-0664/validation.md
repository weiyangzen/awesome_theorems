# Intake validation

Base revision: `a74bf62e5952864a45901ffdf9160b000ba3fd01`.

Validation date: 2026-07-12 (Asia/Shanghai). This validates only target membership, the planned
intake dossier and open task DAG, JSON invariants, scoped local discovery, whitespace, and a narrow
Lean API probe. It is not an exact-statement or proof validation.

The preflight worktree contained the existing untracked `Formalizations/Lean/.lake` link/artifact.
It was used read-only. No update, build, clone, fetch, or other dependency mutation was performed.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0664` | exit 0; rank 708, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| scoped `rg` over repository Lean and pinned mathlib for o-minimality/cell decomposition | exit 0; a legacy assumed-slot discovery module was found, but no pinned mathlib root declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0664/IntakeProbe.lean` | exit 0; generic language, structure, definability, order, interval, finite-family, and disjointness names elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --no-index --check /dev/null` on every new dossier artifact | exit 0 for content checks (the expected no-index difference status was not treated as failure) |

## Status boundary

The exact primary source and theorem variant remain unresolved. Primary-source review, canonical
Lean elaboration and mutation checks, immutable external anchor audit, obligation registry, proof,
composition, trust closure, readable reconstruction, hermetic replay, and independent verification
remain open. These block audit and theorem completion but do not prevent a self-tested `planned`
intake handoff.
