# Intake validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`74980872e6ba4cca3e08b1b728b5cf3695421b94`.

This evidence covers target membership, the planned dossier's fail-closed invariants, JSON syntax,
whitespace, and a narrow Lean elaboration probe of pinned semantic ingredients. It is not the
statement gate and establishes neither derivability nor a completeness proof. The pre-existing
canonical `.lake` artifacts were used read-only; no update, build, clone, fetch, or dependency
mutation was run.

## Environment fingerprint

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0697` | exit 0; rank 738, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned revision recorded above |
| bounded repository and pinned-mathlib searches for the target, completeness, semantic consequence, and derivability | exit 0 overall; catalog ambiguity and semantic/compactness APIs found, but no proof-system derivability or semantic-to-syntactic completeness theorem located |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0697/IntakeProbe.lean)` | exit 0; all eight first-order syntax/semantic API checks elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0697 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0697 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

The first downstream open gate is exact source-statement identity: a primary theorem and formal
proof calculus must be selected and independently reviewed. Canonical Lean elaboration, expression
hashing, transports and mutations, source acceptance, anchor audit, obligation registry, proof,
hermetic replay, readable reconstruction, and independent verification remain open. These prevent
audit and theorem completion but do not invalidate a truthful planned intake.
