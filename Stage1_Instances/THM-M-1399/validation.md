# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical BDF
statement or proof because neither has been frozen. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1399` | exit 0; rank 1009, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10188,10193 -- Docs/researches/math_theorems.md` | exit 0; all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| DOI content negotiation plus Europe PMC metadata query for the two recorded discovery leads | exit 0; bibliographic metadata only; the 1952 article is reported non-open-access and its exact formula/theorem text was not accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1399/IntakeProbe.lean)` | exit 0; five adjacent pinned derivative, ODE, Picard-Lindelof, and polynomial-interpolation APIs elaborated; output SHA-256 `40bb9f8bcde1d64cb5bc47087a569940b60c19efc6336ce83dc6814f2ab580c2`; no target theorem declared |
| exact-topic `rg` search for backward differentiation, BDF method, linear multistep, or stiff equation in pinned mathlib and repo-local Lean | exit 1; expected no match; bounded intake discovery rather than an exhaustive external audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1399/check_intake.py` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1399/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source pins, exact artifact inventory, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `placeholder`, or `fake result` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, an accepted immutable source edition and proposition, complete incorporated
definition/formula/premise/conclusion/proof-boundary/errata crosswalk, method-to-theorem and neighbor
boundaries, and independent source review remain open. So do BDF order, coefficients, normalization,
indexing, grid and step policy, ODE and state-space domain, starting values, implicit-solve policy,
regularity, stability or convergence notion, and all degenerate cases. The canonical Lean expression
and environment fingerprints, checked transports, statement mutations, exhaustive formal anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion also remain open. These
failures do not invalidate a truthful self-tested `planned` intake.
