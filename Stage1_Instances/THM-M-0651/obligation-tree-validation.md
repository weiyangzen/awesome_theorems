# Obligation-tree validation

Item: `S56-M-0651-OBLIGATION_TREE`

The registry and typed graph bundle are generated deterministically from the frozen statement and
anchor-audit artifacts. The checker verifies their input hashes, denominator digest, unique stable
IDs, per-node ledgers and budgets, reciprocal composition edges, acyclic root reachability, typed
edge indexes, validation recipes, and the fail-closed closure boundary.

The narrow Lean probe elaborates the exact target-shaped root, the construction and avoidance
interfaces, and their child-to-parent composition. The composition theorem reports only `propext`
and `Quot.sound`; the interfaces remain premises, so this is composition evidence rather than proof
evidence.

## Commands and results

All commands ran in the worker clone without network access or mutation of `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0651/build_obligation_artifacts.py` | 0 | deterministically wrote 11 obligations and 21 typed edges; denominator `e739a3f3ee963205d34582d0879d767e928e26670f557de0871addcc176f3805` |
| `python3 Stage1_Instances/THM-M-0651/check_obligation_tree.py` | 0 | all registry, graph, ledger, recipe, reachability, and closure-boundary assertions passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0651/ObligationTree.lean` | 0 | root and both interfaces elaborated; `root_compose` axioms: `propext`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets accepted |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697, planned, theorem incomplete |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | all structured artifacts are valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0651` | 0 | no whitespace errors |

## Boundary

The obligation-tree phase is self-tested and pending master acceptance. No mathematical leaf is
closed: the exact root remains `M4`, audit and theorem completion are false, and the open machine
cut set is `L-ENUM`, `L-DENSE`, `L-HENKIN`, and `L-OMIT`.
