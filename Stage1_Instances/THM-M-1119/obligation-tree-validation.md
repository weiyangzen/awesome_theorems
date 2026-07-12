# Obligation-tree validation record

Item: `S56-M-1119-OBLIGATION_TREE`  
Date: `2026-07-12`  
Base revision: `be50e4fee4a4eab420300310f355cd6b1ed3336a`

## Decision

Registry version 1 freezes 15 canonical obligations before proof execution. Thirteen are required
machine obligations and two are non-proof source/provenance overlays. The proof graph separates the
monotone-threshold normalization, finite rectangle construction, planar duality, RSW, Russo's
formula, sharp-threshold package, exact lower and upper bounds, and final equality composition.
Every leaf has an explicit budget at most 100 steps; the high-risk mathematical packages remain
separate rather than being hidden behind a single invocation.

`ObligationTree.lean` checks the only composition currently claimed: exact hypotheses
`(1/2 : NNReal) <= criticalProbability` and `criticalProbability <= (1/2 : NNReal)` jointly imply
the unchanged `KestenTarget`. The axiom report is `[propext, Classical.choice, Quot.sound]`, inherited
from the noncomputable statement environment. Neither inequality has a proof body. Thus the root
remains `M4`, and no theorem, source-review, readability, or release completion is claimed.

## Commands and results

All commands ran in the worker clone. Lean used the existing pinned Lake environment. No update,
build, fetch, clone, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1119/build_obligation_artifacts.py` | 0 | deterministically generated `typed-graphs.json` and `obligation-tree.md` |
| `cd Formalizations/Lean && lake env lean -R ../.. ../../Stage1_Instances/THM-M-1119/Statement.lean -o ../../Stage1_Instances/THM-M-1119/Statement.olean` | 0 | produced a temporary local import artifact for the narrow composition check; removed immediately afterward |
| `cd Formalizations/Lean && LEAN_PATH=../../Stage1_Instances/THM-M-1119 lake env lean -R ../.. ../../Stage1_Instances/THM-M-1119/ObligationTree.lean` | 0 | exact two-bound composition elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1119/check_obligation_tree.py` | 0 | 15 unique obligations, all required node fields, five nonempty typed graphs, budgets, open evidence, and exact composition agree |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | rank 559, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Remaining root cut

The minimal final cut is `M1119-T-SUBCRITICAL` plus `M1119-T-SUPERCRITICAL`. Their upstream open
cut includes monotone threshold normalization and the rectangle/duality/RSW/Russo/sharp-threshold
chain, together with source, provenance, foundation, and readable review gates. Master acceptance
of this architecture cannot supply proof credit for any of those open nodes.
