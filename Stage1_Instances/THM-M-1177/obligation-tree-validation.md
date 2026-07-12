# THM-M-1177 obligation-tree validation

Item: `S56-M-1177-OBLIGATION_TREE`. Base revision:
`446f3e80e7a93deeca70150fa80d9ee079ee0586`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical pinned Lake artifacts and
did not update, build, clone, fetch, or otherwise mutate dependencies.

| Command | Exit | Exact outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1177` | 0 | rank 377; planned; hard mathlib anchor/wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1177/build_obligation_artifacts.py` | 0 | deterministic denominator `fdee2b8bae43f9b17436d494feaf781196712daef92e93a3aa062129f2108ef1` |
| `python3 Stage1_Instances/THM-M-1177/check_obligation_tree.py` | 0 | 21 obligations and 69 typed edges passed; root open at M4 |
| `python3 -m json.tool Stage1_Instances/THM-M-1177/obligation-registry.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1177/typed-graphs.json >/dev/null` | 0 | valid JSON |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-1177 ../../Stage1_Instances/THM-M-1177/Statement.lean -o ../../Stage1_Instances/THM-M-1177/Statement.olean && LEAN_PATH=../../Stage1_Instances/THM-M-1177:$(lake env printenv LEAN_PATH) lake env lean -R ../../Stage1_Instances/THM-M-1177 ../../Stage1_Instances/THM-M-1177/ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; `root_of_architecture` reports `[propext, Classical.choice, Quot.sound]`; only pre-existing unused-variable mutation warnings occurred; temporary `Statement.olean` removed |
| `git diff --check -- Stage1_Instances/THM-M-1177 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The structural checker binds both source hashes, recomputes all frozen denominators, checks unique
IDs, reciprocal proof edges, typed graph indexes, proof-DAG acyclicity and reachability, complete
node ledgers, and the `<=100` budgets. It also rejects Lean placeholder tokens. These checks do not
prove either ABP branch. No accepted receipt is claimed; master acceptance remains required.
