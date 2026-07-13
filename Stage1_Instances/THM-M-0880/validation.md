# THM-M-0880 intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, catalog
provenance, neighbor ownership, pinned environment identity, a narrow Lean API probe, bounded local
search, proof-escape hygiene, JSON integrity, and whitespace. The catalog record is not a
proposition, so elaborating a purported canonical Lean target would invent missing mathematics.
`IntakeProbe.lean` therefore checks adjacent substrate only and supplies no statement or proof
credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was preserved and used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
performed. This is nonrelease worker evidence.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0880` | 0 | rank 1433, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing `Formalizations/Lean/.lake` was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 6446,6451 -- Docs/researches/math_theorems.md` | 0 | all six uncited sparse-cut catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, applicable list, blueprint, DAG, skill, guidelines, both catalogs, Stage0, toolchain, lockfile, and five pinned graph modules | 0 | exact hashes recorded in `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0880/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | eighteen adjacent finite-graph, interedge-density, induced-subgraph, connectivity, and coloring-partition APIs elaborated; four representative axiom reports; output SHA-256 `8dd72c17e1d4db682d5bb25c66cacfd7c14a572537281f18f463196727109f5f` |
| bounded `rg` query for sparse/sparsest cut, cut sparsity, conductance, Cheeger constant, and edge expansion over repo-local Lean and pinned mathlib | 1 | expected no-match; no exact-topic candidate found; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0880-pycache python3 -m py_compile Stage1_Instances/THM-M-0880/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0880/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt, handoff, and six open tasks agree |
| `rg -n --glob '*.lean' '^\s*(sorry\|admit\|axiom\|constant\|opaque\|unsafe)\b\|sorryAx' Stage1_Instances/THM-M-0880` | 1 | expected no-match; no prohibited proof escape declaration |
| `git diff --check`, then `git diff --no-index --check /dev/null <file>` for each untracked changed file | 0 | no whitespace diagnostics; expected no-index difference statuses contained no diagnostics |

## Result and boundary

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector is `[H5, M4, R4]`. The first unmet intake gate is independent integration-lane review and
master acceptance of a node-specific receipt. The first failed theorem gate is statement identity:
the graph and weight model, cut representation, numerator, denominator, positivity and balance
conditions, theorem kind, algorithm and complexity model, and every boundary case remain open.

The separate Arora-Rao-Vazirani catalog row and neighboring flow, cut-algorithm, expander, spectral,
and Cheeger targets supply ownership boundaries only. `SimpleGraph.edgeDensity` uses the
`|S| * |T|` denominator and is adjacent substrate, not a selected sparsest-cut theorem. Exact
source selection, canonical statement elaboration, source/formal anchor audit, obligation freeze,
proof, composition, trust closure, readable reconstruction, hermetic replay, independent
verification, audit completion, and theorem completion remain downstream. Only the integration
lane may accept this provisional intake.
