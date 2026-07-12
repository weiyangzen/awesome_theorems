# THM-M-1148 obligation-tree validation

Item: `S56-M-1148-OBLIGATION_TREE`  
Base revision: `26c19e81aed0ce63fa6787c9db5d397a36f0fb4c`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 26 root-relevant obligations before proof work, with separate inventory,
machine, human-source, and readable denominators. The bundle contains 51 typed edges across proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The validator checks
the complete node schema, denominator digest, reciprocal edge indexes, unique IDs, graph acyclicity,
and reachability of all required obligations from the root.

`ObligationTree.lean` checks the solution-package interface and both directions of the structural
root transport. Its four declarations report only `[propext, Classical.choice, Quot.sound]`. These
are composition interfaces, not implementations of construction or analytic children. The root
remains `M4`, with cut set `M1148-C`, `M1148-L1`, `M1148-B`, and `M1148-N3`.

## Commands and exact outcomes

All commands ran in the worker clone using the existing pinned `.lake` closure. No update, build,
clone, fetch, or dependency mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-1148` | 0 | rank 353, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1148/ObligationTree.lean)` | 0 | interfaces and two-way root transport elaborated; four axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1148/check_obligation_tree.py` | 0 | 26 obligations, 51 typed edges; denominator `a19a68e6...9ad243`; root open M4 |
| `python3 -m json.tool Stage1_Instances/THM-M-1148/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1148/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1148 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This completes only a self-tested architecture freeze pending master acceptance. Planned hashes are
not elaborated proofs; leaf budgets do not establish semantic closure; and the typed composition
consumes an assumed solution package. No analytic proof body, primary-source pinpoint, H0/R0 review,
audit completion, or theorem completion is claimed.
