# Intake validation

Base revision: `94f6abf9359f26384e0f68bef694dc5b9aae624c` (tree
`e0083f4f402c93febe4419b51498afa8ecf81c06`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Jordan-form proposition or proof because neither has been frozen. The
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
| `python3 scripts/stage1_target.py show THM-M-0042` | exit 0; rank 1082, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 321,326 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the author-hosted Axler fourth-edition text | exit 0; Definition 8.44 and Theorems 8.45-8.46 on printed pages 322-324 located; author-hosted PDF digest `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| exact-topic `rg` search for Jordan block, basis, canonical form, or normal form in pinned mathlib and repo-local Lean | bounded search completed; no target declaration found; the only named mathlib theorem family was Jordan-Chevalley-Dunford decomposition, and one repo-local Jordan-block mention was nonproof planning prose |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0042/IntakeProbe.lean)` | exit 0; eight adjacent generalized-eigenspace, Jordan-Chevalley, invertible-matrix, change-of-basis, representation, and block APIs elaborated; stdout SHA-256 `fb397529f72d99215beffb60d06dea6016b944e70072b7a3739c6e3721db7e21`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0042-pycache python3 -m py_compile Stage1_Instances/THM-M-0042/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0042/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, exact artifact hashes, provisional receipt and worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition and exact proposition, the complete Jordan-block and
block-assembly definitions, matrix/operator transport, ordered binders, similarity and ordering
conventions, zero-dimensional and other boundary cases, errata audit, and independent source review
remain open. So do the canonical Lean expression and environment fingerprints, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust and provenance closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.
