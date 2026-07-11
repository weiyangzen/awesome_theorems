# THM-M-0183 obligation-tree validation

Item: `S56-M-0183-OBLIGATION_TREE`. Base revision:
`168aae8f6c98f025672f9f8fcfedb2a74785e4b9`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0183/build_obligation_artifacts.py
  exit 0
  fa96787bf54d8d1f7397f4b0385c8cab1c6ef4d4a866a810e74b61b637dd023c

python3 Stage1_Instances/THM-M-0183/check_obligation_tree.py
  exit 0
  PASS THM-M-0183 obligation tree: 14 obligations, 35 typed edges
  registry denominator sha256: fa96787bf54d8d1f7397f4b0385c8cab1c6ef4d4a866a810e74b61b637dd023c
  root closure: open (M4); prescribed-class Ricci-flat analytic package remains M4

cd Stage1_Instances/THM-M-0183 &&
  LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:"$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
  exit 0
  yauCalabiConjectureTarget_of_analyticPackage depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

The temporary `Statement.olean` was removed after the scoped check. The validator binds the
registry to the exact statement and anchor-audit bytes, recomputes the eligibility denominator,
checks all node ledgers and budgets, checks reciprocal proof edges, graph adjacency and acyclicity,
and validates structured no-network recipes. The Lean check elaborates the exact conditional
child-to-root composition and reports its axioms. It does not prove the analytic package.

This phase freezes architecture only. Root debt remains `[H2, M4, R3]`; audit completion, theorem
completion, accepted receipts, and dependent-phase acceptance remain unclaimed.
