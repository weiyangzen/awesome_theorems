# Obligation-tree validation

Item `S56-M-0649-OBLIGATION_TREE` freezes registry version 1 with 17 unique semantic
obligations and denominator SHA-256
`b1a0f189ba35fe39915c9d436b1dd6da18f1d67fe4c282dd8cf132d36c9f1ef1`. Seven separate typed
graphs contain 84 edges. The checker validates denominator projection, complete node ledgers,
typed endpoints and adjacency indexes, reciprocal proof/composition edges, proof-DAG acyclicity,
required-machine reachability, executable recipe shape, budgets at most 100, and the fail-closed
root boundary.

## Exact commands and results

All commands ran on 2026-07-12 from base revision
`3436a9512b8c720d6b89ba3b8a1d4c405ae3a95f`. The clone is nonrelease-dirty due to these owned
outputs and the automation-provided untracked `Formalizations/Lean/.lake` symlink. That symlink
reuses the canonical pinned artifacts and was not modified.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Stage1_Instances/THM-M-0649/build_obligation_artifacts.py` | 0 | generated 17 obligations, denominator `b1a0f189...f1ef1`, and 84 typed edges |
| repository root | `python3 Stage1_Instances/THM-M-0649/check_obligation_tree.py` | 0 | `PASS`; open M3 root and M4 Tarski-Vaught cut |
| `Formalizations/Lean` | `bash ../../Stage1_Instances/THM-M-0649/check_lean.sh` | 0 | statement module and conditional composition elaborated; composition axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets passed |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0649` | 0 | rank 695, planned, theorem incomplete |
| repository root | `python3 -m json.tool` on all three generated JSON artifacts | 0 each | valid JSON |
| repository root | prohibited-device `rg` scan of `ObligationTree.lean` | 1 | expected negative: no match |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0649 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

`check_lean.sh` writes the intermediate `Statement.olean` only to a fresh temporary directory and
deletes it on exit. No `lake update`, build, dependency clone/fetch, network operation, or `.lake`
mutation was performed.

## Status boundary

`elementaryChainTarget_of_tarskiVaught` checks only exact terminal composition. The formula
induction and hence `CanonicalTarskiVaught` remain open. The first remaining root cut is
`M0649-T-TV`. Primary-source H0 review, formula-induction proof bodies, complete provenance/trust
closure, R0 review, hermetic replay, independent validation, and master acceptance remain open.
Root debt stays H1/M3/R3, and the theorem is not complete.
