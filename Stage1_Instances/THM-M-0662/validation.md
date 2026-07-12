# Intake validation

Base revision: `3436a9512b8c720d6b89ba3b8a1d4c405ae3a95f`.

Validation date: 2026-07-12 (Asia/Shanghai). Validation is limited to target membership, dossier
syntax and invariants, whitespace, scoped discovery searches, and a narrow elaboration probe using
the existing pinned artifacts. The probe checks generic model-theory substrate only. It does not
select or elaborate a canonical simple-theory proposition and supplies no statement or proof
credit.

The preflight worktree contains the existing untracked `Formalizations/Lean/.lake` link/artifact.
It was used read-only. No `lake update`, `lake build`, clone, fetch, or other dependency mutation
was run.

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
| `python3 scripts/stage1_target.py show THM-M-0662` | exit 0; rank 706, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| scoped repository and pinned-mathlib `rg` searches for simple theories, tree property, forking/dividing, and independence theorem | repository metadata and an unrelated Sauer-Shelah result found; no matching model-theoretic root declaration found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0662/IntakeProbe.lean` | exit 0; theories, models, formulas, completeness, satisfiability, complete types, and `typeOf` elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both files are valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0662 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

An accountable source review must select and preserve an immutable primary-source edition, choose
one exact proposition, record theorem/page, definitions, assumptions and errata, and independently
approve the mapping. Canonical Lean elaboration, statement transports and mutations, candidate
audit, obligation registry, proof, hermetic replay, readable reconstruction, and independent
verification all remain open. They prevent audit and theorem completion but do not invalidate a
self-tested `planned` intake.
