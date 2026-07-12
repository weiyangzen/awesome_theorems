# Intake validation

Base revision: `f7de69c04a9761094e2b361e94121e5395124106`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, a narrow local formal-anchor search, and whitespace. No canonical
Lean expression has been selected, so no elaboration or kernel-proof result is claimed. Existing
`.lake` artifacts were read only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1124` | exit 0; rank 564, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| pinned local `rg` search for the authors and Brownian intersection/plane/half-plane exponent terminology | exit 0 for the fail-open search command; no matches in mathlib or repository Lean sources |

Known downstream failures are exact primary-source selection and independent review, canonical Lean
elaboration and mutation tests, formal-anchor audit, obligation registry, proof, hermetic replay,
and release validation. They prevent theorem completion but do not invalidate this fail-closed
planned intake.
