# Intake validation

Base revision: `5a057abd0705ba3f4cadbff1712f2bb7467e6354` (tree
`e6499183859cf75043a1ab13bcce0ca7470a2df6`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source/scope boundary, open task DAG, JSON and scoped
invariants, and a narrow pinned Lean API probe. It does not validate a canonical variational-
equation statement or proof because neither has been frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1341` | exit 0; rank 952, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| bounded inspection of the author-hosted Teschl ODE text and official errata | exit 0; located the distinct initial-state and parameter-sensitivity results recorded in the crosswalk; source-family discovery only, no H0 acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1341/IntakeProbe.lean)` | exit 0; nine adjacent pinned integral-curve, derivative, Frechet-calculus, and continuous-linear-map API checks elaborated; no target theorem declared |
| exact-name `rg` search for `variational equation`, `variation equation`, or `sensitivity equation` in repo-local Lean and pinned mathlib | exit 1; expected no match, discovery only rather than an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `python3 -B Stage1_Instances/THM-M-1341/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source pins, exact artifact inventory and hashes, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, exact immutable source edition and proposition, complete incorporated
definition/premise/conclusion/proof-boundary/errata crosswalk, neighbor-target reconciliation, and
independent source review remain open. So do the canonical Lean expression and environment
fingerprints, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
