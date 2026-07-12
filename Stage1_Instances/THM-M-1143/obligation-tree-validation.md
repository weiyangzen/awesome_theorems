# THM-M-1143 obligation-tree validation

Item: `S56-M-1143-OBLIGATION_TREE`. Base revision:
`24c7a19c1a6033b0aed791e0127a3b3e3564a7b0`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1143/build_obligation_artifacts.py
  exit 0
  af64903cdbdaa77c2ffcbbbf20f444870b91f6e032643c3994d35d2688c20eb7

python3 Stage1_Instances/THM-M-1143/check_obligation_tree.py
  exit 0
  PASS THM-M-1143 obligation tree: 12 obligations, 24 typed edges
  registry denominator sha256: af64903cdbdaa77c2ffcbbbf20f444870b91f6e032643c3994d35d2688c20eb7
  root closure: open (M3); derivative-vanishing and constancy packages remain explicit

lake env lean --version
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-1143 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_vanishingDerivative_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1143
  exit 0: rank 348, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1143 .stage1-worker-selftest.json
  exit 0; no output
```

The failed bare `lake env lean` command is retained as evidence: this clone has no configured Elan
default. The successful narrow retry uses the already-installed pinned Lean 4.29.0 executable and
the `LEAN_PATH` derived by Lake from the existing pinned dependencies.

The checks cover deterministic registry hashes, denominators, node fields, reciprocal proof edges,
typed adjacency, validation-recipe coverage, proof-DAG boundary, Lean elaboration, exact root output,
and the conditional composition's axiom surface. They do not prove either package parameter. No
accepted receipt exists; master acceptance remains required.
