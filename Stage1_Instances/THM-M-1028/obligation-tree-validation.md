# THM-M-1028 obligation-tree validation

Item: `S56-M-1028-OBLIGATION_TREE`. Base revision:
`6f569ca05f8d51664a074ab74399896295f38dee`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1028/build_obligation_artifacts.py
  exit 0
  1da5ac544652c879cb66023728abe4db4292d296422b79c2348bdce03c660d58

python3 Stage1_Instances/THM-M-1028/check_obligation_tree.py
  exit 0
  PASS THM-M-1028 obligation tree: 16 obligations, 35 typed edges
  registry denominator sha256: 1da5ac544652c879cb66023728abe4db4292d296422b79c2348bdce03c660d58
  root closure: open (M2); continuity and nowhere-differentiability packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1028/ObligationTree.lean
  exit 1
  unknown module prefix 'Statement'

cd Stage1_Instances/THM-M-1028 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean
  exit 1
  no default toolchain configured

cd Stage1_Instances/THM-M-1028 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_path_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1028
  exit 0: rank 221, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1028 .stage1-worker-selftest.json
  exit 0; no output
```

The failed invocations are retained as evidence. The successful check used the
already-installed pinned Lean 4.29.0 executable and Lake-derived `LEAN_PATH`.
It validates the exact conditional root composition, its axiom surface,
registry hashes and denominators, complete node schemas, reciprocal proof
edges, graph adjacency, root reachability, recipe coverage, and placeholder
hygiene. It does not prove either open path package. No accepted receipt exists;
master acceptance remains required.
