# THM-M-0821 obligation-tree validation

Item: `S56-M-0821-OBLIGATION_TREE`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

Registry version 2 freezes 36 stable semantic obligations at denominator
`4ea4814dfb5bf3db63946381630ecfa30114c54515612c9e385fa660b53bbc75`. Its
separate attainment and upper-bound routes expand the concrete middle layer and the pinned
`IsAntichain.sperner` body through choose-middle comparison, both LYM formulations,
falling-family induction, shadow incidence bounds, and bipartite double counting. Version 2 records
the append-only addition of the previously hidden falling-zero estimate; the root expression is
unchanged.

Seven typed graphs contain 191 edges with explicit inverse semantics for refinement and trust
relations. Every declared proof child appears in its parent's structured ledger. The 36 ledgers
contain 80 substantive steps, and every budget is at most 100. Six exact package boundaries have
Lean-checked abstract-child composition certificates. Eight internal source-body relations remain
explicitly unverified plans rather than `composes` claims.

`ObligationTree.lean` elaborates the exact packages, conditional compositions, selected middle-layer
ingredients, and the pinned internal declarations used by the planned route. It reports
`IsAntichain.sperner` sorry-free with axiom set `propext`, `Classical.choice`, and `Quot.sound`.
The accepted root remains `[H1, M3, R4]`, with zero closed obligations. Current E2 evidence supports
only M1 candidate status; potential M0-W requires a later accepted E1 proof receipt.

## Commands and exact outcomes

Commands ran from the worker repository root unless a command states another working directory.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0821` | 0 | rank 1379, planned, L0/rework-required, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; exact output SHA-256 `8c616a936e1f6b2689a8955b4904494d5639a105b14cc0154b8805f96d28e97e` |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `python3 -B Stage1_Instances/THM-M-0821/build_obligation_artifacts.py` | 0 | wrote 36 obligations and 191 typed edges; denominator shown above |
| `python3 -B Stage1_Instances/THM-M-0821/check_obligation_tree.py` | 0 | 36 obligations, 191 edges, 80 ledger steps, six certificates, eight open internal plans; Lean-output SHA-256 `46fff72947ef5b3f15531d7e9555869c16e6a5945f2fe535ebbef5481101981e` |
| scoped `lake env which lean`, `lake env printenv LEAN_PATH`, temporary `Statement.olean`, and `lake env lean ../../Stage1_Instances/THM-M-0821/ObligationTree.lean` executed by the checker | 0 | exact package interfaces, conditional compositions, and internal declaration probes elaborated; terminal sorry scan and axiom reports matched |
| `python3 -B` JSON parsing over the four structured JSON artifacts and `ast.parse` over both Python files | 0 | all JSON and Python sources parsed without bytecode output |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus package status and source hashes | 0 | pinned revision/tree matched, the dependency worktree was clean, and four source hashes matched |
| scoped `git diff --check` plus `git diff --no-index --check /dev/null <untracked-file>` for every owned artifact | 0 | no whitespace errors |
| `python3 -B Stage1_Instances/THM-M-0821/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json` | 0 | finalized receipt and worker packet replay passed |

One direct diagnostic command from `Formalizations/Lean` attempted to elaborate
`ObligationTree.lean` before compiling target-local `Statement.lean`; it exited 1 because the
`Statement` module was not then on `LEAN_PATH`. The recorded checker recipe corrects that local
module boundary by compiling a temporary `Statement.olean`, prepending its temporary directory to
the Lake-derived pinned path, and then running `lake env lean`. The temporary directory is removed
automatically. This failed diagnostic supplies no positive evidence.

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

## Known failures

- Intake, statement, and anchor-audit worker evidence still require dependency-ordered master
  acceptance.
- The exact potential M0-W route currently has only E2/M1 candidate evidence; its E1 proof phase
  remains open.
- Eight internal LYM decompositions still require exact child-to-parent composition certificates.
- The no-additional-normalization and no-additional-case-split decisions await independent review.
- Full provenance/TCB closure, primary-source H0, readable R0, hermetic replay, independent
  verification, `AUDIT-Z`, and `THEOREM-Z` remain open.

This is provisional, nonrelease worker evidence for only the assigned obligation-tree freeze. It
accepts no receipt, closes no proof obligation, changes no authoritative checklist state, and claims
neither audit completion nor theorem completion.
