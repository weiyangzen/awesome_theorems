# THM-M-0534 obligation-tree validation

Item: `S56-M-0534-OBLIGATION_TREE`. Base revision:
`79350f6756ac2f7d72136216ef446106f56a6fb9`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0534/build_obligation_artifacts.py
  exit 0
  wrote 14 obligations and 35 typed edges
  e2cff29bb0f36510926e575ac3c4204643092ba53cdbd0975394f93efa929fe3

python3 Stage1_Instances/THM-M-0534/check_obligation_tree.py
  exit 0
  PASS THM-M-0534 obligation tree: 14 obligations, 35 typed edges
  registry denominator sha256: e2cff29bb0f36510926e575ac3c4204643092ba53cdbd0975394f93efa929fe3
  root closure: open (M1); target-owned proof and full trust/provenance closure remain downstream

cd Stage1_Instances/THM-M-0534 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_exactness_families depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0534
  exit 0: rank 591, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0534 .stage1-worker-selftest.json
  exit 0; no output
```

This validates frozen hashes and denominators, the required node schema, typed reciprocal proof
edges, adjacency indexes, proof-DAG reachability, recipe coverage, exact Lean composition, and the
composition certificate's axiom surface. The immediate root cut remains the three imported
exactness-family bridges; their transitive bodies and trust evidence are deliberately not hidden.
There is no accepted receipt, proof-phase closure, audit completion, or theorem completion; master
acceptance remains required.
