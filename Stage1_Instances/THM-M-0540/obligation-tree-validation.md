# Obligation-tree validation

Item: `S56-M-0540-OBLIGATION_TREE`  
Base revision: `d30ab383279f10fe53d90d3c5b5421638c550b25`

The version-1 registry freezes nine obligations and denominator SHA-256
`e845fa732f6d3b06fbbec0c8848b9566a7a3a0f1a847f08094225fffd374b9a7`. The typed bundle contains
24 edges separated across proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. The proof subgraph is acyclic and root-reachable, and every required leaf budget
is at most 100.

## Commands and results

All commands ran on 2026-07-12 in the worker clone. The automation-provided `.lake` link reused the
canonical pinned artifacts and was not modified. No update, build, clone, fetch, or network access
was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and the uniform rework baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0540` | 0 | rank 597, planned lifecycle, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0540/build_obligation_artifacts.py` | 0 | deterministically wrote nine obligations, 24 edges, and the frozen denominator |
| `python3 Stage1_Instances/THM-M-0540/check_obligation_tree.py` | 0 | schema fields, hashes, denominators, reciprocal edges, acyclicity, reachability, recipes, and open-root boundary passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/Statement.lean && lake env lean ../../Stage1_Instances/THM-M-0540/ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; composition axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on the registry, typed graphs, and validation specs | 0 | all three JSON artifacts parsed |
| forbidden-token scan of owned Lean files | 0 | no `sorry`, `admit`, `axiom`, or `sorryAx` token |
| `git diff --check -- Stage1_Instances/THM-M-0540` | 0 | no whitespace errors |

## Status boundary

This self-test validates the obligation freeze and conditional child-to-parent composition only.
It does not convert the anchor-audit candidate into proof credit. `M0540-T-UNFOLD` remains the
minimal open root cut set pending the ordered proof phase, provenance/trust receipts, and master
acceptance. Root state remains `[H1, M3, R4]`; audit and theorem completion are false.
