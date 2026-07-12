# Intake validation

Base revision: `b4d478973911f7d40c96dcd903c8aa1f580291bc`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation covers manifest membership, dossier
structure, scoped intake invariants, and elaboration of pinned mathlib interface names. It does not
establish a canonical statement or any proof. The preflight worktree contained the existing
untracked `Formalizations/Lean/.lake` symlink to the canonical pinned artifacts; it was used
read-only. No `lake update`, `lake build`, clone, fetch, or other dependency mutation was run.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `IntakeProbe.lean` SHA-256: `f979eae4d494e5ea321c4ff4f701e1bda5f3ac0d194f51f27626822d7a9d93ec`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0668` | exit 0; rank 712, planned, hard-statement lane, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0668/IntakeProbe.lean` | exit 0; elaborated `Theory`, `BoundedFormula`, `IsQF`, `toPrenex`, `toPrenex_isPrenex`, and `realize_toPrenex` interfaces |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0668 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

The first downstream blocker is source identity: the inventory row names a property family but no
theory or exact theorem. Primary-source selection and independent review, a canonical Lean target,
mutation tests, formal-anchor audit, obligation registry, proof, readable reconstruction, hermetic
replay, and release validation all remain open. The successful probe establishes only that the
syntax and prenex-normal-form interfaces exist; it provides no quantifier-elimination proof credit.
