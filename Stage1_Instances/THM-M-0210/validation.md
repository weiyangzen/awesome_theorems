# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the open downstream DAG, source provenance, structured intake
invariants, and a narrow pinned Lean API probe. It does not validate a canonical Desargues
proposition or proof because none has been selected. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Platform: Linux `7.0.0-27-generic` x86_64; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0210` | 0 | rank 1226; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1513,1518 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1513,1518p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `f2f4716b5717f4dcc0f719b4b45e17ac5bd2ea8cfaae2b1268ff3d542629ab2e` |
| inspect Magaud-Narboux-Schreck HAL `inria-00432810v2` PDF | 0 | conventional projective statement at printed page 7; independence/dimension boundary and rank/Coq proof at printed pages 20-32; PDF SHA-256 `e8c0c4d2956253a20b63ca944ce9a7cf23eb6756fc7bb44d6ab2381185866bb8`; H1/non-Lean formal lead only |
| inspect Hilbert, *The Foundations of Geometry*, Section 22, Theorem 32, printed page 46 | 0 | affine parallel specialization and converse located; Project Gutenberg PDF SHA-256 `c6f04965b5a8ca67a05c2e969357083b9ec0e7a0a2dd30dbf1ebb025cdcf1161`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| exact-topic `rg` search for Desargues or perspective-triangle declarations in repo-local Lean and pinned packages | 1 | expected no-match result; no target declaration identified; ordinary English uses of “perspective” were separately rejected as unrelated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0210/IntakeProbe.lean)` | 0 | eleven adjacent affine-collinearity, projectivization, projective-subspace, and cross-product interfaces elaborated; stdout SHA-256 `07f989ac9c58115650558ee1ad5764b88d3f3b29ff34a7bfda38378ff69ed483`; no target theorem declared |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0210-pycache python3 -m py_compile Stage1_Instances/THM-M-0210/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0210/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null target, H1/M4/R4 boundary, source and dependency hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0210/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped no-index whitespace checks plus `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

- No independently accepted source selects the point-to-line direction, converse, equivalence, or
  Hilbert affine specialization, nor fixes the incidence model, ambient dimension, scalar or plane
  axioms, correspondence, side meets, concurrency, collinearity, infinity transport, binders, and
  degenerate cases.
- The inspected paper gives strong human and historical Coq evidence, but exact Coq sources,
  revision, toolchain, dependencies, declarations, axioms, and provenance are not in this Lean
  repository's pinned validation closure. It supplies no Lean kernel credit.
- No canonical Lean expression, expression/environment fingerprint, checked alternate encoding, or
  statement mutation suite exists. Adjacent mathlib APIs do not select or prove the root.
- Formal anchor audit, discovery protocol, obligation registry and typed graphs, proof,
  composition, transitive provenance and trust closure, source-faithful reconstruction, hermetic
  replay, deterministic bundle, independent verification, and master acceptance remain open.

These failures block the statement and every completion claim. They do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open task DAG.
