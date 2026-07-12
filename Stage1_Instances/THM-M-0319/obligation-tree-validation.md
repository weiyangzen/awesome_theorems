# Obligation-tree validation

Item: `S56-M-0319-OBLIGATION_TREE`  
Base revision: `28be4ce7383f582503e6b54f645e2ca0e955d9de`

The structural checker recomputes the denominator from the eligibility projection, verifies input
hashes, unique stable IDs, all seven graph families, edge indexes and reciprocal proof edges,
root reachability, acyclicity, semantic ledgers, step budgets, and the fail-closed root boundary.
The Lean probe checks only conditional composition and the zero-dimensional leaf.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && python3 Stage1_Instances/THM-M-0319/build_obligation_artifacts.py` | 2 | Initial operator path was relative to the wrong directory; no file was found and no artifact changed. Corrected below. |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0319/build_obligation_artifacts.py` | 0 | Rebuilt the registry and graphs; denominator `9d15b5eafa794b7f3cc1e83d4006447c90a75f8d8175bbaeb4b50fe8306ccee8`. |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0319/check_obligation_tree.py` | 0 | Passed 12 obligations, 31 uniquely indexed typed edges, reciprocal composition, root reachability, and open-root assertions. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0319/ObligationTree.lean` | 0 | Conditional adapter and dimension-zero leaf elaborated; both axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0319` | 0 | Rank 685, planned lifecycle, theorem incomplete. |
| `python3 -m json.tool` on both generated JSON artifacts | 0 | Both artifacts parsed as JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0319` | 0 | No whitespace errors. |

## Status boundary

This node freezes and self-tests architecture only. The exact external terminal proof body remains
outside the pinned local dependency closure, primary-source mapping and trust closure remain open,
and the root stays `M3`. No proof, validation, release, accepted receipt, or theorem completion is
claimed.
