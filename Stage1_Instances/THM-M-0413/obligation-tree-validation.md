# Obligation-tree validation record

Item: `S56-M-0413-OBLIGATION_TREE`  
Base revision: `e057ea3c85e142707a88ea3fc13445bebddca902`

## Frozen result

Registry version 1 freezes ten required root-relevant obligations and no exclusions. It separates
the exact root, number-field wrapper, generic integral-closure bridge, four defining components,
two prerequisite packages, and the release trust gate. Aliases and the checked integral-closure
transport receive no duplicate denominator or proof-body credit.

The typed bundle separates proof, composition, refinement, provenance, evidence, trust,
documentation, and workflow edges. The mathematical proof graph is acyclic and all nine proof
nodes are root-reachable; the trust node is separate. Three conditional compositions are checked:
all four defining components are consumed by the generic bridge, which supplies the interface,
which supplies the exact root. The four prerequisite-to-component compositions remain open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0413` | 0 | rank 68, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0413/ObligationTree.lean)` | 0 | all three conditional certificates elaborated; `components_compose` reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0413/validate_obligation_tree.py` | 0 | 10 obligations, 12 proof edges, acyclic root reachability, typed graphs, ledgers at most 100 |
| `python3 -m json.tool` on the registry, graph bundle, and proof-unit ledger | 0 | all structured artifacts parse |

An initial composition implementation accidentally selected an existing Dedekind instance, so Lean
warned that three hypotheses were unused. It was rejected as inadequate composition evidence. The
final term explicitly passes all four supplied component instances to the structure constructors;
the successful evidence-bearing run has no unused-premise warning.

## Boundary

This is a narrow, dirty-worktree, nonrelease self-test. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was reused and not modified. No dependency update, build,
clone, or fetch was run. The result freezes and validates the obligation architecture only. It does
not close the component bodies, transitive provenance, human source mapping, readability review,
release trust, audit, or theorem.
