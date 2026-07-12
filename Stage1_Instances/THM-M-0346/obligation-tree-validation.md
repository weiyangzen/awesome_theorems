# THM-M-0346 obligation-tree validation

Item: `S56-M-0346-OBLIGATION_TREE`. Base revision:
`396f523f7db5499e43d86728d9cfe073ac081dfa`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused
read-only; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0346/build_obligation_artifacts.py
  exit 0
  1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5

python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py
  exit 0
  PASS THM-M-0346 obligation tree: 11 obligations, 24 typed edges
  registry denominator sha256: 1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5
  root closure: open (M3); analytic theorem and five transport/integration obligations remain open

cd Stage1_Instances/THM-M-0346 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
  exit 0
  Stage1.THM_M_0346.CarlesonTarget : Prop
  CarlesonTarget : Prop
  root_of_transported_carleson_hunt depends on [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check
```

The structural check validates input hashes, the frozen denominator, eligibility projections,
required node ledgers, all seven graph families, reciprocal proof edges, adjacency, DAG reachability,
the open root boundary, and placeholder hygiene. The Lean check validates the exact result type and
conditional composition against the pinned environment. It does not prove the explicit premise or
any child in the open root cut. Master acceptance remains pending.
