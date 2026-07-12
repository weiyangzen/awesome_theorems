# Intake validation

Base revision: `b4d478973911f7d40c96dcd903c8aa1f580291bc`.

Validation date: 2026-07-12 (Asia/Shanghai). Validation is limited to target membership, dossier
structure and invariants, pinned API discovery, JSON syntax, and whitespace. `IntakeProbe.lean`
elaborates names needed to design a later statement; it does not elaborate the canonical target or
prove quantifier elimination.

The preflight worktree contained the existing untracked `Formalizations/Lean/.lake` artifact. It was
used read-only. No `lake update`, `lake build`, clone, fetch, or dependency mutation was performed.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0669` | exit 0; rank 713, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned revision recorded above |
| scoped repository and pinned-mathlib searches for real-closed-field quantifier elimination | exit 0; generic syntax, Presburger elimination, and algebraic real-closed-field APIs found, but no target declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0669/IntakeProbe.lean` | exit 0; printed checked types for `IsRealClosed`, ring-language syntax, realization, theory equivalence, and models |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0669 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source inspection and independent review, canonical
statement elaboration and mutation tests, formal-candidate audit, obligation registry, proof,
hermetic replay, readable reconstruction, and independent release verification. They prevent audit
and theorem completion but do not invalidate a truthful planned intake.
