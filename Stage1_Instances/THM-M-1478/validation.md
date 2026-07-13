# Intake validation

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical L-stability proposition or proof because neither has been frozen. The
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
| `python3 scripts/stage1_target.py show THM-M-1478` | exit 0; rank 1155, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10784,10789 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Hairer-Wanner Crossref metadata and author-hosted books page, table of contents, and corrections | exit 0; IV.3 pages 40-49 separates the stability function, A-stability, and L-stability; the correction sheet changes a page-98 L-stability parameter range; source-family lead only |
| bounded Ehle DOI observation | no retained response or hash; uncredited search lead only, not admitted validation evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` over relevant pinned mathlib and repo-local Lean | exit 0 due only to unrelated model-theory omega-stability prose; no L/A-stability, Runge-Kutta, stability-function/region, amplification-factor, Dahlquist, or Radau target declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1478/IntakeProbe.lean)` | exit 0; sixteen adjacent complex-limit, rational-function, matrix, and ODE APIs elaborated; stdout SHA-256 `b666076db0ff86f8f2f4f5d7fed24ead6c3e9742cbfa2e96150b879cf7598456`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1478-pycache python3 -m py_compile Stage1_Instances/THM-M-1478/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1478/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source/dependency pins, artifact hashes, provisional receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0 after finalization; no whitespace errors |

## Known open gates

An accepted immutable source and exact truth-valued proposition, complete method/problem and
stability-function definitions, pole and implicit-stage-solvability policy, A-stability component,
limit filter or path, conclusion, quantifier order, exceptional cases, relevant corrections,
neighbor ownership, and independent source review remain open. So do the canonical Lean expression
and environment fingerprints, checked transports, statement mutations, exhaustive formal anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.
