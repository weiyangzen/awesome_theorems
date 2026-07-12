# THM-M-0168 obligation-tree validation

Item: `S56-M-0168-OBLIGATION_TREE`  
Base revision: `89d346c6e4d70a887dc4caa607fa8e82a9050b47`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

Registry version 1 contains eleven unique canonical obligations. It freezes the exact root, the
statement interface, graph construction, PDE-to-minimality transport, stability, logarithmic
cutoffs, curvature vanishing, derivative rigidity, affine integration, source provenance, and
trust boundary. Eligibility and denominators were fixed without using proof availability. The
Lean harness defines the two top-level open packages as propositions and proves only their
conditional composition into the exact root.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | rank 665, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0168/build_obligation_artifacts.py` | 0 | deterministically generated registry and graph bundle |
| `python3 -m json.tool Stage1_Instances/THM-M-0168/obligation-registry.json >/dev/null` | 0 | registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0168/typed-graphs.json >/dev/null` | 0 | graph bundle is valid JSON |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | all schemas, budgets, denominators, internal endpoints, proof acyclicity, root composition edges, open root, and cut set passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0168/ObligationTree.lean` | 0 | exact open package types and `compose_root` elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `rg -n '\\b(sorry\|axiom\|admit\|native_decide)\\b' Stage1_Instances/THM-M-0168/ObligationTree.lean` | 1 | expected no-match result: no forbidden proof-gap or custom-axiom token |
| `git diff --check -- Stage1_Instances/THM-M-0168 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Validated content hashes:

- `obligation-registry.json`: `883e0c0a98c6d3b6e5e77adb9c5fb376c87f043dd7b80b4e882cbdb0045ed9ba`
- `typed-graphs.json`: `1e8ac1d8a5906eccbd79a35b43fad6e89ee571fa4ee0bc5aa0e6b08894dcac41`
- `ObligationTree.lean`: `642153a1f88af5d71a954b417b136fd95d1eaf82b8d1fdf176d60b3ace3bf24e`

The root remains `M2`; all theorem-bearing children are open. No dependency fetch, `.lake`
mutation, proof implementation, authoritative state edit, H0/M0/R0 claim, or theorem-completion
claim was performed. This node is self-tested and remains provisional pending master acceptance.
