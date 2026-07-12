# Obligation-tree validation

Item: `S56-M-1286-OBLIGATION_TREE`  
Worker base revision: `b8f3bf167e30c3816a5c83c67dd1844ea5f08787`

Validation uses only the existing pinned Lean environment. No update, build, fetch, clone, or
mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1286/build_obligation_artifacts.py` | 0 | generated 18 obligations and the typed graphs deterministically |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | schema fields, frozen hashes, denominator, reciprocal proof edges, reachability, acyclicity, recipes, and open-root boundary passed |
| `lake env lean -R ../.. -o /tmp/thm-m-1286-obligation/Stage1_Instances/THM-M-1286/Statement.olean ../../Stage1_Instances/THM-M-1286/Statement.lean` (from `Formalizations/Lean`) | 0 | exact statement compiled to an isolated temporary olean |
| `LEAN_PATH=/tmp/thm-m-1286-obligation lake env lean ../../Stage1_Instances/THM-M-1286/ObligationTree.lean` (from `Formalizations/Lean`) | 0 | planned package signatures and exact child-to-root composition elaborated; axiom report contains only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest valid |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | rank 457, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/obligation-registry.json >/dev/null` | 0 | registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/typed-graphs.json >/dev/null` | 0 | graph bundle is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1286 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The obligation-tree phase is self-tested but pending master acceptance. The theorem is not proved
or complete; both analytic packages in the frozen root cut set remain open.
