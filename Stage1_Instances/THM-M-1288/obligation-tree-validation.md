# THM-M-1288 obligation-tree validation

Item: `S56-M-1288-OBLIGATION_TREE`. Base revision:
`c326cc33b70825386f90cf5d885ad451004fbbff`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No dependency update, fetch, clone, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1288/build_obligation_artifacts.py` | 0 | Generated registry, typed graphs, validation recipes, and readable tree; denominator `89405ccd...55eb4` |
| `python3 Stage1_Instances/THM-M-1288/check_obligation_tree.py` | 0 | PASS: 19 obligations and 43 typed edges; root open at M3 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1288/Statement.lean` | 0 | Exact frozen target re-elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1288/ObligationTree.lean` | 1 | Expected module-path failure: `Statement` was not in this invocation's search path; no proof result credited |
| `LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd Stage1_Instances/THM-M-1288 && LEAN_PATH="$LEAN_PATH" $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=".:$LEAN_PATH" $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean; rm -f Statement.olean` | 0 | Scoped exact Lean 4.29.0 elaboration passed; conditional composition axioms: `propext`, `Classical.choice`, `Quot.sound`; temporary olean removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1288` | 0 | Rank 459, planned, theorem incomplete |
| `python3 -m json.tool` on the four structured obligation artifacts | 0 | All JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-1288 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The structural check recomputes the frozen denominator, validates all required
node fields and budgets, checks typed endpoint adjacency and reciprocal
`proof_requires`/`composes` edges, rejects proof cycles, checks recipe coverage,
and confirms the open root cut set. The Lean check establishes only that exact
admissibility and optimality package hypotheses compose to the exact root.

No analytic package proof is claimed. `M1288-T-ADMISSIBILITY` and
`M1288-T-OPTIMALITY` remain the root cut set; H0, R0, transitive trust closure,
proof closure, release validation, and theorem completion remain open. Master
acceptance is required before the provisional worker state can be promoted.
