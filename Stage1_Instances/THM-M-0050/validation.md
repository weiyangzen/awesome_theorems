# Intake validation

Base revision: `c76fe0f1a7514b41f191d16840eff25e64ee9d17` (tree
`388bc991837bae9741d7e7cb88b43c216eab966a`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical inertia proposition or proof because neither has been frozen. The automation-provided
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
| `python3 scripts/stage1_target.py show THM-M-0050` | exit 0; rank 1089, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 377,382 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the author-hosted Treil 2017 text | exit 0; Chapter 7 Section 3 and Theorem 3.1 on printed pages 206-208 inspected; PDF digest `d4659dd7b1c1f9d6a8f78cda7a636354d191eb8a8cbd40f12042d59e83c4074f`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| bounded exact-topic search of pinned mathlib and repo-local Lean | completed; signature/equivalence, real diagonalization, and matrix congruence interfaces located; no exact catalog-ratified matrix declaration credited |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0050/IntakeProbe.lean)` | exit 0; eleven adjacent APIs elaborated; stdout SHA-256 `5ca2a7332ba033e2df9c61c5e3f834f2c6194dc0488d0f73673a5c1339e77a74`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0050-pycache python3 -m py_compile Stage1_Instances/THM-M-0050/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0050/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and DAG identity, null target, H1/M3/R4 boundary, pins, artifact hashes, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no prohibited declaration or placeholder matched |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition and exact proposition, real/Hermitian specialization,
matrix/quadratic-form transport, matrix domain and symmetry binders, congruence witness and
orientation, inertia definitions, zero-index policy, all boundary cases, errata audit, and
independent source review remain open. So do the canonical Lean expression and environment
fingerprints, checked transports, statement mutations, exhaustive anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful
self-tested `planned` intake.
