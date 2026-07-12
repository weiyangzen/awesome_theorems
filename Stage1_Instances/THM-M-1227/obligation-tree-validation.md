# THM-M-1227 obligation-tree validation

Base revision: `8e91b4fe8c825b493e2620c859148fe9685db568`.

Validation uses only the repository's existing pinned Lean and `.lake` artifacts. No update, build,
clone, fetch, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1227` | 0 | rank 416; planned; theorem_complete false |
| `python3 Stage1_Instances/THM-M-1227/build_obligation_artifacts.py` | 0 | generated 21 obligations and 63 typed edges |
| `python3 Stage1_Instances/THM-M-1227/check_obligation_tree.py` | 0 | registry fingerprints, denominators, node schema, graph reciprocity/reachability/acyclicity, recipes, and open boundary passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1227/Statement.lean` | 0 | canonical target and conditional six-conjunct composition elaborated; Lean reports `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on the three generated JSON artifacts | 0 | all are valid JSON |
| `rg -n '(^|[^[:alnum:]_])(sorry|admit|sorryAx)([^[:alnum:]_]|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1227 --glob '*.lean'` | 1 | expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1227` | 0 | no whitespace errors |

The composition check is conditional and provides no existence proof. All 21 obligations remain
uncredited; root state stays `M4`, with formalization, primary-source, readable, hermetic, and
independent-review work open. This is a self-tested obligation-tree node pending master acceptance.
