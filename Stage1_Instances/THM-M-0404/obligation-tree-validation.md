# THM-M-0404 obligation-tree validation

Item: `S56-M-0404-OBLIGATION_TREE`. Base revision:
`5e34bb84b4b5122c40ec88ebb411d9499433e123`.

Validation ran from the worker clone on 2026-07-12. The existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0404/build_obligation_artifacts.py
  exit 0
  9626018721df387abb21cc86d86a977ba5472fb851c23ea9f47f88d25f44d785

python3 Stage1_Instances/THM-M-0404/check_obligation_tree.py
  exit 0
  PASS THM-M-0404 obligation tree: 15 obligations, 31 typed edges
  registry denominator sha256: 9626018721df387abb21cc86d86a977ba5472fb851c23ea9f47f88d25f44d785
  root closure: open (M3); eventual-periodicity and combinatorial packages remain M4

cd Stage1_Instances/THM-M-0404 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0404 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_eventualPeriodic_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0404
  exit 0: rank 17, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0404
  exit 0; no output
```

The failed `lake env lean` invocation is recorded rather than hidden: Lake can
read the pinned dependency environment, but the clone has no Elan default. The
successful retry uses the exact pinned Lean 4.29.0 executable already installed
on this machine and the same Lake-derived `LEAN_PATH`.

This validates registry hashes, frozen denominators, required node fields,
typed reciprocal proof edges, graph adjacency, proof-DAG reachability, recipe
coverage, hygiene, elaboration, exact root output, and the conditional
composition's axiom surface. It does not prove either explicit package premise.
There is no accepted receipt; master acceptance remains required.
