# THM-M-0652 obligation-tree validation

Item: `S56-M-0652-OBLIGATION_TREE`. Base revision:
`d9657b35845b4b10e25345050fe228f872bc50ad`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, fetch, clone, or dependency build was run.

```text
python3 Stage1_Instances/THM-M-0652/build_obligation_artifacts.py
  exit 0
  generated 15 obligations; denominator 4eb4a0414633ed491ed194764d56fd06b048e59c0d4609a852845f09b68b5d15

python3 Stage1_Instances/THM-M-0652/check_obligation_tree.py
  exit 0
  PASS THM-M-0652 obligation tree: 15 obligations, 36 typed edges
  registry denominator sha256: 4eb4a0414633ed491ed194764d56fd06b048e59c0d4609a852845f09b68b5d15
  root closure: open (M3); completeness, syntactic interpolation, and soundness remain explicit

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0652/ObligationTree.lean
  exit 1
  unknown module prefix 'Statement'

cd Stage1_Instances/THM-M-0652 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean
  exit 1
  no default toolchain configured

cd Stage1_Instances/THM-M-0652 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  statement_of_calculus_packages depends on axioms: [Quot.sound]
  Statement.olean removed after the scoped check
```

The direct command could not resolve the adjacent module. The first scoped
retry exposed the clone's missing Elan default. The successful retry uses the
already-installed pinned Lean 4.29.0 binary with Lake's pinned `LEAN_PATH`;
these failures are recorded rather than hidden.

The checks validate content hashes, frozen denominators, typed reciprocal proof
edges, graph adjacency and acyclicity, root reachability, node ledgers and step
budgets, source hygiene, elaboration, exact root output, and the conditional
composition axiom surface. They do not close any of its three premises. No
accepted receipt exists; integration-lane review and master acceptance remain
required.
