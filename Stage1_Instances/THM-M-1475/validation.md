# Intake validation

Base revision: `f4efdfc7c685252a98f3508a5974ba81c0377a95` (tree
`94a9cfc613f86042a21fdfa174ba887334b93893`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Runge-Kutta stability proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
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
| `python3 scripts/stage1_target.py show THM-M-1475` | exit 0; rank 1152, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10763,10768 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Hairer-Wanner author-hosted book metadata, contents, and corrections | exit 0; explicit-RK stability at IV.2 pages 15-37, implicit stability functions/A/L stability at IV.3 pages 40-49, and a later L-stability correction located; source-family lead only |
| bounded inspection of immutable Driscoll-Braun online source | exit 0; commit `000839af87622138c210a6361ba05913705ffbe4`, Chapter 11 absolute-stability source digest `ec0d0c6477d14a74546cf6edcb1508e222be4e92d4f7466822d1e18065bfcaa8`; source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | exit 1 as expected; no named Runge-Kutta, Butcher-tableau, absolute-stability, stability-function, or stability-region declaration under the recorded terms; intake discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1475/IntakeProbe.lean)` | exit 0; ten adjacent complex, finite-matrix, rational-function, and ODE APIs elaborated; stdout SHA-256 `92a7ac79a0315e35b078aace6e8a560bfac0d396f40e85e2b37697c68956a9ad`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1475-pycache python3 -m py_compile Stage1_Instances/THM-M-1475/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1475/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source/dependency pins, artifact hashes, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0 after finalization; no whitespace errors |

## Known open gates

An accepted immutable source and exact proposition, complete tableau/equation/stability-function
definitions, function-domain and invertibility conditions, stability predicate and conclusion,
quantifier order, exceptional cases, relevant corrections, neighbor ownership, and independent
source review remain open. So do the canonical Lean expression and environment fingerprints,
checked transports, statement mutations, exhaustive formal anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
