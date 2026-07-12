# THM-M-1141 obligation-tree validation

Item: `S56-M-1141-OBLIGATION_TREE`. Base revision:
`3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-1141/build_obligation_artifacts.py
  exit 0
  6f4e5fa64e6d8750ab7592a5b54a269a3b0759b480fae5c802c9740e5daef2d1

python3 Stage1_Instances/THM-M-1141/check_obligation_tree.py
  exit 0
  PASS THM-M-1141 obligation tree: 11 obligations, 67 typed edges
  registry denominator sha256: 6f4e5fa64e6d8750ab7592a5b54a269a3b0759b480fae5c802c9740e5daef2d1
  root closure: open (M3); analytic and compact-chain packages remain M4

cd Stage1_Instances/THM-M-1141 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-1141 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean ObligationTree.lean
  exit 0
  harnackInequality_of_uniformValueComparison depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

The failed direct Lake invocation is retained as evidence: Lake provides the
pinned dependency path, but this clone has no default Elan toolchain. The
successful retry uses the already installed pinned Lean 4.29.0 executable and
the same Lake-derived `LEAN_PATH`. The temporary `Statement.olean` was removed.

Structural validation covers source hashes, the frozen denominator, node
fields, step budgets, typed-edge adjacency, reciprocal proof edges, validation
recipe coverage, hygiene, and the open-root boundary. Kernel validation covers
the exact conditional composition and its axiom surface. It does not prove the
uniform comparison premise. Master acceptance remains required.
