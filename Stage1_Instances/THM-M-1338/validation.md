# Intake validation

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5` (tree
`ae4ad4de219b61476e1ed10c008e8139247b9d77`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source/scope boundary, open task DAG, JSON and scoped
invariants, and a narrow pinned Lean API probe. It does not validate a canonical Bihari-LaSalle
statement or proof because neither has been frozen. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no update, build, clone, or fetch operation was run.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
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
| `python3 scripts/stage1_target.py show THM-M-1338` | exit 0; rank 949, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| bounded Crossref and Springer metadata retrieval for DOI `10.1007/BF02022967` | exit 0; authenticated I. Bihari, title, journal, volume 7 issue 1, pages 81-94, 1956, DOI; response hashes are recorded in `instance.json` |
| attempted publisher PDF retrieval | transport exited 0 but `file` identified a paywall HTML document, not a PDF; no primary theorem text was credited |
| bounded Crossref retrieval for DOI `10.2307/1969559` | exit 0; authenticated the 1949 LaSalle bibliographic candidate only |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1338/IntakeProbe.lean` | exit 0; six adjacent pinned Gronwall and interval-integral APIs elaborated; no target theorem declared |
| bounded `rg` name search for Bihari, LaSalle, nonlinear/generalized Gronwall in repo-local Lean and pinned mathlib | exit 1; expected no match, discovery only rather than an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `python3 -B Stage1_Instances/THM-M-1338/check_intake.py` | exit 0; manifest identity, null target, H1/M4/R4 boundary, exact artifact inventory and hashes, receipt, self-test, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

The exact primary result, complete primary text, definition and premise mapping, Bihari/LaSalle
relationship, errata review, and independent source review remain open. So do the canonical Lean
expression and fingerprints, statement mutations, formal anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These failures do not invalidate a truthful self-tested `planned` intake.
