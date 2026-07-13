# Intake validation

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical GMRES proposition or proof because neither has been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1454` | exit 0; rank 1131, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10616,10621 -- Docs/researches/math_theorems.md` | exit 0; all six sparse catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the primary Saad-Schultz paper | exit 0; Algorithm 3, equations (3)-(8), Propositions 1-4, Theorem 5, and Corollaries 3 and 6 located; scan SHA-256 `4e90d7387751887455ee519208e83d8f40dc4b8972e4ea382d9a51e7c7db387d`; result-family source lead only, while the catalog target remains H5 until made a stable proposition |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` searches in pinned mathlib and repo-local Lean | no GMRES or generalized-minimal-residual declaration found; this is not an exhaustive external anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1454/IntakeProbe.lean)` | exit 0; ten adjacent matrix-vector, Gram-Schmidt, span, projection, norm, and dot-product APIs elaborated; no target declaration or proof body exists |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1454-pycache python3 -m py_compile Stage1_Instances/THM-M-1454/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1454/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source and dependency pins, exact artifact inventory and hashes, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, an accepted immutable primary-source proposition, complete incorporated
definition/premise/conclusion/correction crosswalk, algorithm and restart boundary, exact-arithmetic
scope, and independent source review remain open. So do the canonical Lean expression and
environment fingerprints, checked transports, statement mutations, exhaustive formal anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures do not invalidate a
truthful self-tested `planned` intake.
