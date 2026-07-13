# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the open downstream DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Morley proposition or proof because none
has been frozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

The Taylor-Marr PDF was downloaded only for bounded source inspection. It was not added to the
repository or admitted as accepted H0 evidence or a dependency. The structured validation recipes
use only repository and already pinned Lean inputs with network denied.

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
| `python3 scripts/stage1_target.py show THM-M-0205` | 0 | rank 1537; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1478,1483 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1478,1483p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `3edff88c4f0ed403e3a12b2a210b6884c3edcd475ad424a363ae262d803878b2` |
| inspect Taylor-Marr, DOI `10.1017/S0013091500035100`, Section 2, printed page 119 | 0 | exact internal side-adjacent statement and complete proof routes located; Cambridge PDF SHA-256 `3d8603772297831131307442eb8400e210b9d07fe82e446573e7e963575bba5d`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| bounded exact-topic `rg` search for Morley, trisector, trisection, or angle-trisection declarations | 0 | only two unrelated model-theory search strings for “Morley rank” were found; no geometry target declaration identified; output SHA-256 `6b3261d626edf1bef9c18ec09c6040c2d02b3dbde2e04c28b450698eb1d5a78b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0205/IntakeProbe.lean)` | 0 | thirteen adjacent angle, distance, collinearity, betweenness, congruence, simplex-interior, and equilateral interfaces elaborated; stdout SHA-256 `eb97c71a17fa4197b066faf959eb06b887f16f0c749f81d8c329cab756c264ea`; no target theorem declared |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0205-pycache python3 -m py_compile Stage1_Instances/THM-M-0205/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0205/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null target, H1/M4/R4 boundary, source and dependency hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0205/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON duplicate-key scan over owned JSON and `.stage1-worker-selftest.json` | 0 | strict `object_pairs_hook` parser found no duplicate keys |
| scoped no-index whitespace checks plus `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

- No independently accepted source edition has fixed the exact ambient plane and ordered
  nondegenerate triangle, internal ray versus line convention, cyclic side-adjacent pairs,
  intersections, equilateral encoding, diagram cases, corrections, errata, or historical 1899
  attribution.
- No canonical Lean expression, expression/environment fingerprint, checked alternate encoding,
  or statement mutation suite exists. Adjacent mathlib APIs do not select or prove the root.
- The conclusion must preserve the source's nondegenerate "triangle DEF" boundary: bare equal
  distances could admit three coincident witnesses, while a bundled `Affine.Triangle` requires an
  affine-independence construction.
- Formal anchor audit, discovery protocol, obligation registry and typed graphs, proof,
  composition, transitive provenance and trust closure, source-faithful reconstruction, hermetic
  replay, deterministic bundle, independent verification, and master acceptance remain open.

These failures block the statement and every completion claim. They do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the source and ambiguity boundary and open
the downstream task DAG.
