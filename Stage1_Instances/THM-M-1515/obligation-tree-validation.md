# THM-M-1515 obligation-tree validation

Item: `S56-M-1515-OBLIGATION_TREE`. Base revision:
`5a2ecdada3f8494f880f308f251e71f9e8184441`.

Validation ran in the worker clone on 2026-07-12. It reused existing pinned Lake artifacts. No
dependency update, build, fetch, or clone was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1515
  exit 0: rank 184, planned, theorem_complete false

python3 Stage1_Instances/THM-M-1515/build_obligation_artifacts.py
  exit 0
  fd9b5fe11f610a06d7bc94ac848a1247bdee31d15abb2992ad020d9f727e3eb2

python3 Stage1_Instances/THM-M-1515/check_obligation_tree.py
  exit 0
  PASS THM-M-1515 obligation tree: 12 obligations, 41 typed edges
  registry denominator sha256: fd9b5fe11f610a06d7bc94ac848a1247bdee31d15abb2992ad020d9f727e3eb2
  root closure: open (M3); two analytic derivative packages remain M4

cd Stage1_Instances/THM-M-1515 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1: no default toolchain configured

cd Stage1_Instances/THM-M-1515 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_derivative_packages depends on axioms: [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check
```

The initial `lake env lean` failure is retained as evidence: Lake exposes the pinned dependency
environment, but this clone has no Elan default. The retry uses the installed executable matching
the pinned Lean 4.29.0 toolchain and the same Lake-derived `LEAN_PATH`.

The checks validate source-bound hashes, the frozen denominator, required node fields, typed graph
adjacency, reciprocal proof/composition edges, proof-DAG acyclicity and reachability, prohibited-token
hygiene, elaboration, exact root output, and the conditional composition axiom surface. They do not
prove either analytic package. Master acceptance remains required.
