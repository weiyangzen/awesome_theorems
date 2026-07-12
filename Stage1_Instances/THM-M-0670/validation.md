# Intake validation

Base revision: `f489f107e7abbb49376144c22d5e41ece02d20ea`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation covers target membership, dossier
structure, and elaboration of a discovery-only Lean API probe. It does not elaborate a canonical
statement and establishes no proof closure.

The preflight worktree contained the existing untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`, clone, fetch, or
other dependency mutation was performed.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0670` | exit 0; rank 714, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | exit 0; pre-existing untracked `Formalizations/Lean/.lake` recorded |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| bounded `rg` searches for Presburger, Ackermann, and quantifier elimination in pinned mathlib | exit 0; relevant APIs and a Presburger QE TODO found, but no terminal Presburger QE declaration |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0670/IntakeProbe.lean)` | exit 0; all seven pinned declarations elaborated and their types were printed |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped intake invariant assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0670 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

The first failed downstream gate is exact-statement identification: the source must determine the
language expansion, standard-model versus theory-relative semantics, and existence versus verified
algorithm formulation. Until then the canonical Lean expression, alternate transports, source
acceptance, formal-candidate audit, obligations, proof, reconstruction, hermetic replay, and
independent verification remain open. This does not block completion of the planned intake.
