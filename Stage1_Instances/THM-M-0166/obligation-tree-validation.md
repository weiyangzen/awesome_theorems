# THM-M-0166 obligation-tree validation

Item: `S56-M-0166-OBLIGATION_TREE`  
Base revision: `bd4f335d8afb4d242d9df61f9d79a60034c17dfc`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

Registry version 1 contains seven unique canonical obligations. Its typed proof graph exposes the
distance substrate, completeness-to-compactness package, global minimizer, subsegment-minimality,
exact root composition, and trust boundary. The Lean harness elaborates the two open package types
and a conditional composition theorem; it contains no assertion of either open package.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard passed for all 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest uniqueness and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0166` | 0 | rank 122, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0166/obligation-registry.json >/dev/null` | 0 | registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0166/typed-graphs.json >/dev/null` | 0 | graph bundle is valid JSON |
| `python3 Stage1_Instances/THM-M-0166/check_obligation_tree.py` | 0 | seven node schemas, budgets, denominators, typed endpoints, open root, cut set, and composition edges passed |
| `lake env lean ../../Stage1_Instances/THM-M-0166/ObligationTree.lean` from `Formalizations/Lean` | 0 | open package propositions and `compose_root` elaborated; axiom report was exactly `propext`, `Classical.choice`, `Quot.sound` |
| `git diff --check -- Stage1_Instances/THM-M-0166 .stage1-worker-selftest.json` | 0 | no whitespace errors |
| Lean proof-token scan over `ObligationTree.lean` | 0 | no forbidden declaration or proof-gap token |

Content hashes recorded after validation:

- registry: `b646b364e4db6b21d3a5f98793d90c65e7bad3e8f38100471cab0d5cd7af9b3c`
- typed graphs: `6933b3009479827ae69053397d2bea8d8b0d8c287de09a62481621ee2eb9f2d7`
- Lean harness: `d1d0335e729e9c103a65efd40b06aca3d1f9bdd69f3b18636cd79068e0f6a1a2`

No dependency fetch, `.lake` mutation, proof implementation, state edit, or theorem-completion claim
was performed. This self-tested node remains provisional pending master acceptance.
