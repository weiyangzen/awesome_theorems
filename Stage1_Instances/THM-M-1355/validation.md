# Intake validation

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, catalog/source boundary, open task DAG, structured
invariants, and a narrow pinned Lean API probe. It does not validate a canonical linear-stability
statement or proof because no exact proposition has been selected. The automation-provided
canonical `.lake` symlink existed before the intake and was used read-only; no dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1355` | exit 0; rank 965, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree shown above |
| source record, Stage0, manifest, blueprint, DAG, skill, and neighbor inspection | exit 0; located the sparse catalog gloss, all proposition-changing omissions, and distinct neighbor targets; no source-selected proposition |
| bounded inspection of Teschl's author-hosted ODE text and official errata | exit 0; found distinct bounded-stability, asymptotic-stability, exponential-estimate, and stable-subspace results; source-family discovery only, no H0 acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision and tree recorded above; package worktree clean |
| `sha256sum` over authority, source, toolchain, lock, and probed mathlib source inputs | exit 0; hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1355/IntakeProbe.lean)` | exit 0; ten adjacent matrix-exponential, spectral, and integral-curve APIs elaborated without declaring a target theorem |
| bounded exact-topic search in pinned mathlib and repository-local Lean | exit 1, expected no match; found no target-specific stability declaration; intake discovery only, not an exhaustive external audit |
| JSON parse, Python syntax, and scoped intake checker | exit 0; target/DAG identity, null target, planned H1/M4/R4 boundary, pins, exact artifact inventory, receipt/packet agreement, and six open tasks passed |
| prohibited Lean construct scan over the owned path | exit 1, expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks | exit 0; every changed artifact passed without diagnostics |

## Known open gates

Canonical root selection, an accepted immutable source proposition, complete incorporated
definition/premise/conclusion/proof-boundary/errata mapping, neighbor-target reconciliation, and
independent source review remain open. So do the canonical Lean expression and environment
fingerprints, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
