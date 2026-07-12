# THM-M-0329 obligation-tree validation

Item: `S56-M-0329-OBLIGATION_TREE`  
Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`

Validation ran in the worker clone on 2026-07-12 using only the existing pinned
Lake artifacts. No update, build, dependency clone, or fetch was run.

The structural checker regenerates and verifies the statement and anchor freeze
hashes, immutable registry denominator, eligibility projections, graph
adjacency, reciprocal proof/composition edges, proof-DAG acyclicity, per-node
validation recipes, step budgets, placeholder hygiene, and the explicit open
root boundary. Lean separately checks the exact typed package-to-root
composition. This is node-specific self-test evidence, not proof acceptance or
theorem completion.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0329/build_obligation_artifacts.py` | 0 | generated registry, typed graphs, and validation specs; denominator `852bdc59e2ed4e06290a11ef592640475a71292a1111e2a19947e149f3ce0308` |
| `python3 Stage1_Instances/THM-M-0329/check_obligation_tree.py` | 0 | 17 obligations, 67 typed edges, matching denominator, and explicitly open root |
| scoped pinned Lean command recorded below | 0 | `root_of_packages` elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0329` | 0 | rank 822, planned, theorem incomplete |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | valid JSON |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b|sorryAx' Stage1_Instances/THM-M-0329 -g '*.lean'` | 1 expected | no prohibited placeholder or axiom declaration |
| `git diff --check -- Stage1_Instances/THM-M-0329 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The exact Lean invocation obtains the pinned executable and `LEAN_PATH` from
`lake env`, compiles `Statement.lean` to a temporary olean inside the owned
directory, checks `ObligationTree.lean`, and removes the temporary olean:

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0329
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
```

## Status boundary

The obligation registry and typed graphs are self-tested pending master
acceptance. The exact root is not accepted as closed. Proof-body binding,
primary-source mapping, transitive trust/provenance closure, hermetic replay,
independent review, release receipts, full audit, and theorem completion remain
open.
