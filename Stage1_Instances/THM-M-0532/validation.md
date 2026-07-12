# Intake validation

Base revision: `8cd5bc5a3f94397a9ec5148db97a8631552f37ec`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, and whitespace. No canonical Lean expression has been selected,
so no elaboration or kernel-proof result is claimed. Existing `.lake` artifacts were used read only;
no update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0532` | exit 0; rank 589, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository and pinned-mathlib `rg` search for Kunneth spellings and product-homology/Tor phrases | mixed 0/1; found repository metadata and a mathlib documentation title, but no theorem-specific Lean declaration; no absence claim beyond this narrow search |
| `python3 -m json.tool` on both owned JSON files | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0532 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact source selection and independent review, canonical Lean
elaboration and mutation tests, exhaustive anchor audit, obligation registry, proof, hermetic replay,
and release validation. They prevent theorem completion but do not invalidate this fail-closed
planned intake.
