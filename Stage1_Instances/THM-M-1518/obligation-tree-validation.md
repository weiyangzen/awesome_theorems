# THM-M-1518 obligation-tree validation

Validated on 2026-07-12 in the worker clone at base revision
`ff80c1f55ecdfa168e5feec2a8b1b65960177ea0`. Lean used only the existing
pinned Lake environment; no dependency update, build, clone, or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1518/build_obligation_artifacts.py` | 0 | deterministically wrote 12 obligations; denominator `dc5ea1db...02b1` |
| `python3 Stage1_Instances/THM-M-1518/check_obligation_tree.py` | 0 | hashes, schemas, denominators, 26 typed edges, reciprocity, root reachability, acyclicity, leaf budgets, recipes, and open-root boundary passed; the exact statement and conditional composition elaborated; axioms were `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 consistent |
| `python3 scripts/stage1_target.py show THM-M-1518` | 0 | rank 187, planned, L0/rework-required, theorem incomplete |
| `rg -n 'sorry|admit|axiom |sorryAx' Stage1_Instances/THM-M-1518/ObligationTree.lean Stage1_Instances/THM-M-1518/build_obligation_artifacts.py` | 1 | expected no-match; no forbidden proof construct |
| `git diff --check -- Stage1_Instances/THM-M-1518 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validator creates a temporary `Statement.olean` outside the repository,
adds only that temporary directory to `LEAN_PATH`, runs `lake env lean` on the
owned tree module, then removes the directory. It does not mutate `.lake`.

## Boundary

This phase freezes the denominator and validates only conditional composition.
The minimal open root cut set is `M1518-N-DIFFERENTIATE`, `M1518-L-IBP`, and
`M1518-L-FUNDAMENTAL`; root status remains `M4`. There is no proof, audit,
release, or theorem-completion claim. Master acceptance is still required.
