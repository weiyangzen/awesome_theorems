# Obligation-tree validation

Node `S56-M-1129-OBLIGATION_TREE` freezes registry version 1 with 22 unique semantic
obligations and denominator SHA-256
`407e6cd04e60f8d98703a6983c13fd9847ad694685a4951e88a33d39292dd3bd`. The seven separate
typed graphs contain 75 edges. The checker validates complete node schemas, denominator
projections, graph endpoints and adjacency indexes, reciprocal proof/composition edges, proof-DAG
acyclicity, required-machine reachability, budgets at most 100, and the fail-closed root boundary.

## Exact commands and results

All commands ran on 2026-07-12 from repository revision
`8a434aa49a78627cb0f9ce260ee33af4d1f2f174`. The clone was nonrelease-dirty solely because the
automation-provided untracked `Formalizations/Lean/.lake` symlink reuses the canonical pinned Lake
artifacts and because of this node's owned outputs.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Stage1_Instances/THM-M-1129/build_obligation_artifacts.py` | 0 | deterministically generated 22 obligations and denominator `407e6cd0...d3bd` |
| repository root | `python3 Stage1_Instances/THM-M-1129/check_obligation_tree.py` | 0 | `PASS`; 22 obligations, 75 typed edges, open M3 root and M4 analytic package |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-1129/ObligationTree.lean` | 0 | conditional composition elaborated; axiom report was exactly `propext`, `Classical.choice`, `Quot.sound` |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-1129/Statement.lean` | 0 | exact canonical target still elaborated and all four statement mutations were rejected |
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-1129` | 0 | rank 334, planned, hard-mathlib-anchor-and-wrapper lane, theorem incomplete |
| repository root | `rg -n '(^|[[:space:]])(sorry\\|admit)([[:space:]]|$)\\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1129/ObligationTree.lean` | 1 | no prohibited proof-device match |
| repository root | `python3 -m json.tool Stage1_Instances/THM-M-1129/obligation-registry.json` | 0 | valid JSON |
| repository root | `python3 -m json.tool Stage1_Instances/THM-M-1129/typed-graphs.json` | 0 | valid JSON |
| repository root | `git diff --check -- Stage1_Instances/THM-M-1129 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Status boundary

`poissonFormulaTarget_of_analyticPackage` checks only exact child-to-parent composition. Its
explicit premise `PoissonAnalyticPackage` is definitionally the complete canonical target and is
still open; it is not a proof shortcut or root closure. The first remaining proof cut is
`M1129-T-REPRESENT`. Primary-source H0 review, every substantive analytic proof body, provenance and
trust closure, readable R0 review, hermetic replay, independent validation, and master acceptance
remain open. Root debt stays H2/M3/R3 and the theorem is not complete.
