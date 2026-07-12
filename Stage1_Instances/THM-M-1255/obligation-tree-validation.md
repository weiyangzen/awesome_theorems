# THM-M-1255 obligation-tree validation

Item: `S56-M-1255-OBLIGATION_TREE`  
Base revision: `66ea3415424fb2dd9f2dc93a957a93df337749e6`

## Result

The frozen registry contains 13 unique semantic obligations and a stable denominator digest.
Seven separate typed graphs cover proof, refinement, provenance, evidence, trust, documentation,
and workflow relations. Every proof-requirement edge has a checked reciprocal composition edge,
the proof graph is acyclic and root reachable, and every semantic node has a step ledger of at most
100 steps.

`ObligationTree.lean` elaborates the action and fundamental-solution package interfaces and checks
their conditional composition into the exact `MalgrangeEhrenpreisTarget`. It contains no proof of
either package and therefore gives no root proof credit. The root remains `M3`; the minimal open cut
is `M1255-C-ACTION` plus `M1255-C-FUNDSOL`.

## Validation

All commands ran in this automation clone. Lean ran from `Formalizations/Lean` using the existing
pinned `.lake` artifacts. No update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1255/ObligationTree.lean` | 0 | conditional package interfaces and exact-root composition elaborated; axiom report contained only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1255/check_obligation_tree.py` | 0 | 13 obligations, 25 typed edges, frozen denominator, reciprocal proof edges, acyclicity, root reachability, recipes, and open closure boundary validated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned, L0/rework-required, theorem incomplete |
| forbidden-term scan of `ObligationTree.lean` | 1 | no `sorry`, `admit`, `axiom`, or `sorryAx` occurrence; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1255 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is a self-tested obligation-tree receipt pending master acceptance. It does not close proof,
source fidelity, trust, provenance, readability, hermetic replay, or theorem-release gates.
