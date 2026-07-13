# THM-M-0820 intake validation

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2` (tree
`dfc20d8141f18f6b09a03e818acfff408e836714`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-family and cover/partition boundary, scope map,
open task DAG, JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a
canonical THM-M-0820 expression or proof because primary-source review and exact representation
selection belong to the dependent statement phase. The automation-provided canonical `.lake`
symlink pre-existed this work and was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, or other `.lake` mutation was performed. This dirty worker packet is nonrelease
evidence.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0820` | 0 | rank 1378, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| Crossref inspection of the 1971 Mirsky article metadata | 0 | exact bibliography identified; linked full text was not usable and is not credited as inspected primary evidence |
| inspection of arXiv `1703.10977v1`, printed pages 3-4, 7-8, and 18-19 | 0 | finite inhabited carrier, maximum-chain cardinality, possibly overlapping antichain cover, and printed Coq target crosswalk recorded; secondary/Coq source only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean identity recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake identity recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned source was clean |
| bounded target search over repository Lean and pinned mathlib | 0 search; target matches absent | no lexical Mirsky declaration or target-specific antichain-cover/chain-height bridge found; not an exhaustive anchor audit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0820/IntakeProbe.lean` | 0 | eight pinned interfaces plus empty and singleton chain-height boundaries elaborated; stdout SHA-256 `18168f39b271d0df6e607b6b29707a9b9c7931e5530f3271e130beaf54a8cd53`, empty stderr |
| `python3 -m json.tool` on all owned JSON artifacts and the root worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0820-pycache python3 -m py_compile Stage1_Instances/THM-M-0820/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0820/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source pins, null target, H1/M3/R4 boundary, artifact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0820/check_intake.py` | 0 | public replay mode passed |
| prohibited-construct scan over `IntakeProbe.lean` | 1 expected no-match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token found |
| scoped per-new-file whitespace checks plus `git diff --check` | 0 | no whitespace errors |

## Evidence boundary

The Lean probe proves only that named pinned declarations and two representation boundaries
elaborate. It does not freeze a Mirsky root, prove the minimum-cover equality, transport cover to
partition, or inspect terminal proof bodies. Primary-source theorem/proof/errata inspection and
independent review, exact statement and mutation suite, exhaustive candidate/provenance audit,
obligation registry and typed graphs, proof and composition, readable reconstruction, hermetic
replay, deterministic evidence bundle, and independent verification remain open. These boundaries
prevent audit and theorem completion but do not invalidate a self-tested `planned` intake.
