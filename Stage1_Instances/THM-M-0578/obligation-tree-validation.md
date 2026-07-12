# THM-M-0578 obligation-tree validation

Item: `S56-M-0578-OBLIGATION_TREE`. Base revision:
`83c1cc0af3ba7bd4612988241849d2949fad9e72`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0578/build_obligation_artifacts.py
  exit 0
  67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda

python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py
  exit 0
  PASS THM-M-0578 obligation tree: 13 obligations, 28 typed edges
  registry denominator sha256: 67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda
  root closure: open (M4); construction, homeomorphism, and nondiffeomorphism remain open

cd Stage1_Instances/THM-M-0578 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0578 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_exoticWitnessPackage depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0578
  exit 0: rank 622, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0578
  exit 0; no output
```

The failed `lake env lean` invocation is retained as evidence. Lake supplies
the pinned dependency environment, but this clone has no Elan default. The
successful retry uses the installed pinned Lean 4.29.0 executable and the same
Lake-derived `LEAN_PATH`.

These checks cover deterministic artifact generation, denominator hashes,
eligibility partitions, semantic ledgers, typed reciprocal proof edges, graph
adjacency, proof-DAG acyclicity, recipe coverage, placeholder hygiene, Lean
elaboration, conditional child-to-parent composition, and its axiom surface.
They do not close any of the three mathematical root-cut nodes. Master
acceptance remains outstanding.
