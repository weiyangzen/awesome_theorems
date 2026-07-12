# Obligation-tree validation record

Item: `S56-M-0708-OBLIGATION_TREE`  
Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`  
Date: `2026-07-12` (`Asia/Shanghai`)

## Frozen result

Registry version 1 contains 13 canonical obligations with denominator SHA-256
`8d03f26719e0e3448bd84500bdcf9ec97fe65ec6dd437441e09ec08cca2642e7`. Seven
separate graph families contain 30 typed edges. The checked composition consumes an explicit
`RiceBridge` and yields the exact re-elaboration of the frozen root. The bridge remains the root cut
until the proof phase adopts the audited pinned candidate.

## Validation

Commands ran from the repository root unless a subshell is shown. No Lake dependency operation or
build was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0708/build_obligation_artifacts.py` | 0 | deterministically wrote 13 obligations and 30 typed edges; denominator digest matched |
| `python3 Stage1_Instances/THM-M-0708/check_obligation_tree.py` | 0 | registry hashes, required node schema, graph endpoints/reciprocity/acyclicity, recipes, root cut, and forbidden-token scan passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0708/ObligationTree.lean)` | 0 | exact conditional composition elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0708` | 0 | rank 749, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0708 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` canonical-cache materialization was not
modified. This is nonrelease worker evidence pending master acceptance. Audit completion, proof
adoption, root closure, independent validation, release, and theorem completion are not claimed.
