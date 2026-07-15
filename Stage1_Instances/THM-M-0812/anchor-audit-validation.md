# THM-M-0812 anchor-audit validation

Item: `S56-M-0812-ANCHOR_AUDIT`

Base revision: `647eb08e6581ada8fde2fbcd0c9e58e142d3dc72`

Base tree: `1a7772398b00170f5a21c9b4dc1bf30de0cebb0c`

Validation date: `2026-07-15` (`Asia/Shanghai`)

## Result

The ten frozen candidate groups are classified. The exact two-sorted finite-incidence statement
remains `M3`: pinned mathlib supplies simple-graph bipartiteness, matching and vertex-cover
predicates, an attained `ENat` vertex-cover minimum, and Hall matching theorems, but it has no
maximum-matching number or Konig matching-cover equality. The audit probe repeats the exact target,
checks ten adjacent interfaces, and makes Lean reject two proof-bearing declarations at the root
type. Four inspected pinned declarations are sorry-free and depend only on `propext`,
`Classical.choice`, and `Quot.sound`.

The strongest public leads are not eligible proof bodies. ATLAS has `SimpleGraph.konig_theorem`
under the same Lean/mathlib pins, but its project report exposes `sorryAx` through the concrete
`sorry` at `Berge.lean:685`; its one-sorted `ENat` statement also lacks checked exact-target
composition and its license is restrictive. Closed, unmerged mathlib PR 33032 has the closest
placeholder-free source family, `SimpleGraph.Konig.konig_bipartite[_fin]`, at immutable head
`6cfc4b1f...`. It uses Lean 4.28.0-rc1 and a different dependency lock, fails against the current
pin, has no native kernel/axiom receipt in this packet, assumes supplied extrema, and still needs
representation, attainment, and cardinality transports. Neither candidate receives `M1` or `M0`.

## Commands and results

All local checks used the automation-provided canonical `.lake` symlink read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout, install, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0812` | 0 | rank 1371; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | immutable base recorded; only the automation `.lake` symlink predated this packet |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C ... status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean worktree |
| bounded `rg`, tracked-tree, package-tree, and pinned-history searches for Konig and matching-cover aliases | expected bounded no exact match | 2827 repo Lean paths, 7871 mathlib sources, and 9676 materialized package sources classified |
| immutable raw-source inspection of Formal Conjectures, ATLAS, and mathlib PR 33032 | mixed completed/access failures | support-only, placeholder-blocked, and unintegrated/toolchain-blocked candidates classified; no saturation claim |
| current-pin replay of PR 33032 source | 1, expected blocker | pinned Matching lacks PR APIs; attempted import-path adaptation also fails across changed APIs; no recovered declaration credited |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0812/Statement.lean` | 0 | frozen statement freshly elaborated; stdout SHA-256 `e9c73fc4...c450e` |
| `cd Formalizations/Lean && LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0812/AnchorAudit.lean` | 0 | exact target copy, ten interfaces, two expected type mismatches, four sorry/axiom reports; stdout SHA-256 `27903d96...d997` |
| `LC_ALL=C LANG=C NO_COLOR=1 python3 -B Stage1_Instances/THM-M-0812/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | authority, statement identity, pins, hashes, ten classifications, receipt, packet, and both Lean replays agree |
| JSON parse, Python AST parse, comment-aware forbidden scan, per-file whitespace checks, and scoped `git diff --check` | 0 | structured artifacts valid; adapter has no proof escape; no whitespace diagnostics |

## Status boundary

This phase supplies provisional self-tested anchor evidence pending dependency-ordered master
acceptance. It freezes no obligation tree, integrates no external dependency, accepts no proof or
receipt, and establishes no complete transitive trust closure. Human-source `H0`, readable `R0`,
`AUDIT-Z`, hermetic release validation, independent verification, and theorem completion remain
open. The authoritative root vector stays `[H1, M3, R2]`.
