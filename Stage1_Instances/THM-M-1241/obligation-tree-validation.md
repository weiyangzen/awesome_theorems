# THM-M-1241 obligation-tree validation

Item: `S56-M-1241-OBLIGATION_TREE`. Base revision:
`883205204cea57181965a9de9620f3c150aaf2e8`.

Validation ran from the worker clone on 2026-07-12. It reused the existing
pinned Lake artifacts; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1241/build_obligation_artifacts.py
  exit 0
  d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e

python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py
  exit 0
  PASS THM-M-1241 obligation tree: 15 obligations, 31 typed edges
  registry denominator sha256: d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e
  root closure: open (M3); finite-exponent and infinite-endpoint packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1241/ObligationTree.lean
  exit 1
  expected setup failure: `import Statement` requires a scoped `Statement.olean`

cd Stage1_Instances/THM-M-1241 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean
  exit 1
  environment setup failure: no default Elan toolchain configured

cd Stage1_Instances/THM-M-1241 &&
  LEAN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LP=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN_PATH="$LP" "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:"$LP" "$LEAN" ObligationTree.lean
  exit 0
  root_of_finite_and_endpoint_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check
```

The successful Lean command obtains both the pinned executable and dependency
path from the existing Lake environment. The conditional theorem splits on
`q < infinity` and `r < infinity`, preserves every canonical binder and
hypothesis, and returns the exact canonical target. Both analytic packages are
explicit premises, so this is composition evidence rather than proof credit.

The structural validator checks input hashes, frozen denominators, unique IDs,
required typed-node fields and step ledgers, reciprocal proof edges, adjacency,
acyclic root reachability, validation-recipe coverage, placeholder hygiene,
and the fail-closed root status. Master acceptance remains required; there is
no accepted receipt, audit completion, or theorem completion.
