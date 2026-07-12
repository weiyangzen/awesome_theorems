# THM-M-0698 obligation-tree validation

Item: `S56-M-0698-OBLIGATION_TREE`  
Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

Validation ran on 2026-07-12 in the worker clone. It reused the existing pinned
Lake dependency closure read-only. No update, build, fetch, clone, or dependency
mutation was performed.

## Results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0698/build_obligation_artifacts.py` | 0 | wrote 16 obligations and 45 typed edges; denominator `ff7e990e...f61a4` |
| `python3 Stage1_Instances/THM-M-0698/check_obligation_tree.py` | 0 | registry hashes, frozen denominators, required fields, reciprocal edges, adjacency, acyclicity, reachability, recipes, and open-root boundary passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0698/ObligationTree.lean` | 0 | forward implication and conditional exact-root composition elaborated; both axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0698` | 0 | rank 739, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool` on the three generated JSON artifacts | 0 | all valid JSON |
| prohibited-token scan over `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-0698 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These checks validate the obligation freeze and conditional composition only.
`M0698-B-REVERSE` remains the root cut at M4 in this phase. The matching pinned
mathlib theorem is recorded as provenance but is not promoted to proof credit.
H0, R0, audit completion, theorem completion, release replay, and master
acceptance all remain open.
