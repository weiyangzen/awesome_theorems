# Intake validation

Base revision: `53ef4456383f8ae0068669a633bb02c08056bce8` (tree
`d88aafa961abcd157b3f589fa1eaf2d675c2395d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and duplicate-scope boundary, open task DAG,
JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Poincare-Bendixson statement or proof because neither has been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1348` | exit 0; rank 959, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| bounded inspection of the author-hosted Teschl ODE text and official errata | exit 0; located the distinct Lemma 7.13 and generalized Theorem 7.16 roots and the material page-222 erratum recorded in the crosswalk; source-family discovery only, no H0 acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1348/IntakeProbe.lean)` | exit 0; eleven adjacent pinned integral-curve, flow, omega-limit, invariance, and periodic-point API checks elaborated; no target theorem declared |
| exact-topic `rg` search for Poincare-Bendixson or Bendixson in pinned mathlib | exit 0 only for unrelated Cantor-Bendixson prose; no terminal target declaration; bounded intake discovery rather than an exhaustive external audit |
| exact-topic `rg` search in repo-local Lean | exit 0; only the legacy `THM-M-1400` file appeared, and that file expressly denies terminal proof credit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1348-pycache python3 -m py_compile Stage1_Instances/THM-M-1348/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1348/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source pins, duplicate boundary, exact artifact inventory and hashes, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, an accepted immutable source edition and proposition, complete incorporated
definition/premise/conclusion/proof-boundary/errata crosswalk, `THM-M-1400` duplicate reconciliation,
and independent source review remain open. So do the canonical Lean expression and environment
fingerprints, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
