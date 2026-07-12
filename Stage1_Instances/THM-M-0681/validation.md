# Intake validation

Base revision: `c62c7e6f4b9f2eace4ef9d3f7e3e90240c96391f`.

Validation date: 2026-07-12 (Asia/Shanghai). Validation is limited to target membership, dossier
structure and invariants, pinned API discovery, JSON syntax, and whitespace. `IntakeProbe.lean`
does not elaborate a canonical axiomatization or establish proof closure.

The preflight worktree contained the existing untracked `Formalizations/Lean/.lake` artifact. It was
used read-only. No `lake update`, `lake build`, clone, fetch, or dependency mutation was performed.

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
| `python3 scripts/stage1_target.py show THM-M-0681` | exit 0; rank 722, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned revision recorded above |
| bounded `rg` searches for differential fields, differential polynomials, differential closedness, and `DCF` in pinned mathlib | exit 0; ordinary differential-field APIs found, but no differential-polynomial interface or terminal axiomatization declaration |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0681/IntakeProbe.lean)` | exit 0; all five pinned ingredient declarations elaborated and printed their types |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0681 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

The first downstream failed gate is exact-statement identification. Primary-source inspection must
select the axiom scheme and map it to existential closedness; Lean also lacks a located
differential-polynomial interface for expressing the expected scheme. Until those are resolved,
canonical expression hashing, mutations, accepted source mapping, anchor audit, obligation tree,
proof, hermetic replay, readable reconstruction, and independent verification remain open. These
failures do not invalidate this truthful planned intake.
