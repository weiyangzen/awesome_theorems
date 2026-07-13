# THM-M-1459 intake validation

Base revision: `58fbed45d2c785466ee920c7696f0f7b3686d9a5` (tree
`36198f7c90045b3b21d338a3d0ce47aa4ff930f1`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical fast multipole proposition or proof because no source-selected root exists. The
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
| `python3 scripts/stage1_target.py show THM-M-1459` | exit 0; rank 1136, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10651,10656 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref lookup for DOI `10.1016/0021-9991(87)90140-9` | exit 0; publisher metadata located the 1987 article; observed response digest `6be90529ec44dbd32cea883cf1baec3968ee896cb3120e2b4262e673da4740b8`; article body not inspected |
| bounded inspection of Greengard's publication page, the Beatson-Greengard short course, and the Carrier-Greengard-Rokhlin 1988 adaptive follow-up | exit 0; observed digests `6665bf314afda2c47bed2bc0275f15cd21c6e8eb7d36416603942ef76f3a1bd7`, `2691e493b4cebc167573dc3db12f9d568a724ecd0469b7c92d068ed2a2db1128`, and `a49ce4a647fb29a7701c0e8db58c250f13f6f7d3fe3dca94d2b765b39f1333d1`; distinct analytic, translation, hierarchy, cost, storage, and empirical claims confirmed; discovery leads only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | expected no-match exit 1; no fast-multipole-, multipole-, Greengard-, or Rokhlin-named declaration found; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1459/IntakeProbe.lean)` | exit 0; nine adjacent finite-sum, geometric-series, complex-norm, and logarithmic Taylor/remainder APIs elaborated; stdout SHA-256 `3b73bb355540cf5aaf30c21257f47cbb4f69f6e825b1dcbe6576ddce9a95eef6`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1459-pycache python3 -m py_compile Stage1_Instances/THM-M-1459/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1459/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1459 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped new-file no-index whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The static or dynamic task, dimension, kernel, particle and strength data, collision policy,
hierarchy, separation rules, expansion and translations, accuracy and cost models, arithmetic
semantics, ordered binders, conclusion, neighbor boundaries, and degenerate cases remain open. So
do the canonical Lean expression and environment fingerprint, checked transports, statement
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust/provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
