# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical Courant
min-max statement or proof because neither has been frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1390` | exit 0; rank 1000, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10125,10130 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref/zbMATH metadata lookup plus inspection of the Zenodo `2131750` scan | exit 0; identified Courant's 1920 paper and Section 3, Satz 3a, pages 18-19 as a strong historical source lead; temporary scan SHA-256 `21452389...f7764`; discovery only, no H0 admission |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1390/IntakeProbe.lean)` | exit 0; nine adjacent pinned Rayleigh/spectral APIs elaborated; output SHA-256 `d72f106fdad67f031173510e8eb0da9f646acaf24d5b9bf1a47ae8e807a2d550`; no target theorem declared |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | exit 1; expected no match for Courant/Fischer or eigenvalue-minimax declarations; intake discovery rather than exhaustive audit |
| `python3 -m json.tool` on all owned JSON and the root worker packet | exit 0 after finalization |
| Python `ast.parse` on `check_intake.py` | exit 0; validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1390/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, current source and dependency hashes, null target, H1/M4/R4 boundary, exact inventory, packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for proof escapes or unsafe declarations |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, repository-owned immutable primary-source admission, exact German
transcription and translation, complete incorporated definition/premise/conclusion/proof-boundary
and correction crosswalk, historical-PDE-to-modern-operator relationship, and independent source
review remain open. So do the canonical Lean expression and environment fingerprints, minimal
imports, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
