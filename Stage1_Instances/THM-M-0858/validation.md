# Intake validation

Base revision: `561d83df037004ceb2259292d7c63be930b40391`; base tree:
`6eb02475bf5a70139d60615c924b31c930efc2bb`. Validation date: 2026-07-13
(Asia/Shanghai); exact timestamps are recorded in the provisional receipt.

This validates only the `S56-M-0858-INTAKE` planned dossier: target membership, catalog
provenance, original-source and modern-form boundaries, the scope and crosswalk, open task DAG,
pinned graph-coloring substrate, and representability of a deliberately noncanonical
source-shaped envelope. It does not validate a canonical Brooks statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or
other `.lake` mutation was performed. The owned files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

Crossref metadata and the Cambridge publisher's first-page facsimile were inspected for DOI
`10.1017/S030500410002168X`. They confirm R. L. Brooks, the paper title, volume 37 issue 2, April
1941, pages 194-197, and expose the exact theorem paragraph on printed page 194. That paragraph
fixes `n > 2`, pointwise degree at most `n`, looplessness, componentwise exclusion of an
`n`-simplex, `n`-colorability, and the permission for infinite nonplanar networks.

No external source was added to the repository. The complete four-page source and proof were not
lawfully preserved in the dossier; network versus simple-graph semantics, possible parallel
lines, proof premises, corrections and errata, and independent review remain open. Consequently
the source is an H1 lead and not an H0 packet.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0858` | 0 | rank 1412, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6292,6297 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and Cambridge publisher inspection for DOI `10.1017/S030500410002168X` | 0 | bibliographic identity and printed-page-194 theorem text inspected; first-page facsimile SHA-256 `10837123a6d5f8a87d70fdfe6628799a0710ab4cd6efe292717e282f281ee9c4` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version, platform and commit recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded; package status empty |
| `sha256sum` on authority, source, toolchain, lock, and three probed mathlib source modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0858/IntakeProbe.lean)` | 0 | nine pinned APIs plus `IsNSimplex` and `Brooks1941SourceEnvelope` elaborated; output SHA-256 `ae01b6d6eb28dffbcbf1e960cb59bfc3b0f83b9268c1fe128e9086d7e0f716ca`; no theorem or proof body |
| bounded exact-target `rg` search over repo-local and pinned-mathlib Lean | 1 (expected no match) | no Brooks or degree-to-colorability target declaration found; intake discovery only, not exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every finalized structured artifact is valid JSON |
| `python3 -c` using `ast.parse` on `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0858/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null canonical target, H1/M3/R4 boundary, source/dependency hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet, plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only for ordinary new-file differences with empty diagnostics |

## Known open gates

Complete immutable source admission, proof and premise crosswalk, graph/multigraph model decision,
parallel-edge and degree semantics, corrections and errata review, independent source review,
canonical target and minimal imports, expression/environment fingerprints, checked transports, and
all four statement mutation classes remain open. So do exhaustive anchor/provenance audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures block the statement
phase but do not invalidate a truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0858-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
