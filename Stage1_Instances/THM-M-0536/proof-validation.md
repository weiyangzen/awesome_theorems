# THM-M-0536 proof-phase validation

Item: `S56-M-0536-PROOF`. Base revision:
`0d96c69f4ed36252336c9f7f535191869f854cf6`.

## Implemented closure

`Proof.lean` proves the exact frozen proposition. It constructs the inverse of the homology map of
`e.toFun` as the homology map of `e.invFun`. The declarations `induced_left_identity` and
`induced_right_identity` use the two packaged homotopies, the pinned mathlib theorem
`TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor`, and functoriality to establish the
two inverse equations. `homotopyInvariance` installs those equations in `IsIso`.

The target body is checked textually against `Target.lean`. There is no premise added to the root,
no replacement theorem, and no placeholder, axiom declaration, or unsafe declaration. The local
source hash is `7a512d0b2d6a6d518b32d6697cda476f85159a5d575a1ed66f7cd8718b5a6b83`.

## Narrow validation record

All commands ran in the worker clone on 2026-07-12 and reused the existing canonical pinned Lake
artifacts. No update, build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0536` | 0 | Rank 593, planned, theorem incomplete before master acceptance. |
| `python3 Stage1_Instances/THM-M-0536/check_obligation_tree.py` | 0 | Frozen 15-node obligation registry and typed graphs passed. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0536/Target.lean` | 0 | Exact target elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0536/Proof.lean` | 0 | Both inverse laws and exact root elaborated; all three axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-0536/check_proof.py` | 0 | Exact target equality, declarations, receipt hash, and prohibited-token scan passed. |
| `git diff --check -- Stage1_Instances/THM-M-0536 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Status boundary

This is provisional, self-tested proof-phase root closure only. It supports the later validation
node but does not perform hermetic replay, source/readability acceptance, independent verification,
or release. `theorem_complete` remains false, and only the master may accept the receipt or update
the generated execution state.
