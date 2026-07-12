# Intake validation

- Item: `S56-M-1560-INTAKE`
- Base revision: `110eef5926707beba105078ad2163c88ae8bf0e8`
- Validation date: 2026-07-12 (Asia/Shanghai)

Validation is limited to manifest consistency, the truthful `planned` dossier, JSON syntax, scoped
intake invariants, pinned-environment discovery, and whitespace. The exact source theorem is not yet
selected, so there is no canonical Lean expression to elaborate and no kernel-proof claim.

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
worker clone exposes `Formalizations/Lean/.lake` as an untracked link to canonical pinned artifacts;
it existed before this item and was only read for the narrow environment and mathlib searches.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1560` | 0 | Rank 571, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...8b81` respectively |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` for `Deift-Zhou`, nonlinear/ordinary steepest descent | 0 | Only target metadata was found; no theorem-specific local Lean artifact |
| pinned-mathlib `rg` for Riemann-Hilbert, steepest descent, modified KdV, and oscillatory jumps | 1 | No match; exit 1 is the expected negative-search result |
| `curl -L --max-time 20` of the official Annals article record | 0 | HTTP 200; title, authors, 1993, volume 137 issue 2, pages 295-368, and DOI confirmed |
| `python3 -m json.tool` on both owned JSON files | 0 | Valid JSON |
| scoped Python intake assertions | 0 | Planned lifecycle, empty accepted states, null exact target, root vector, and six ordered open tasks confirmed |
| `git diff --check -- Stage1_Instances/THM-M-1560` | 0 | No whitespace errors |

## Known downstream failures

- No numbered primary-source theorem, exact premise/conclusion map, proof-boundary audit, errata
  disposition, or independent mathematical review is frozen.
- Consequently the exact Lean target, minimal imports, expression/environment fingerprints,
  checked transports, and statement mutation tests do not exist.
- The formal anchor audit, obligation registry, proof, composition, trust audit, readable
  reconstruction, hermetic replay, and independent verification remain open.

These gates prevent any theorem-completion claim. They do not invalidate a self-tested planned
intake whose purpose is to freeze the honest scope boundary and open the dependent task DAG.
