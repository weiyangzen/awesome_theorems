# THM-M-0509 obligation-tree validation

Item: `S56-M-0509-OBLIGATION_TREE`. Base revision:
`e9252b1cfdc99a094324c8a10d260769df2eca15`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0509/build_obligation_artifacts.py
  exit 0
  74b4c30d82e3aa7c44f356d24eb5cd21c2d48ce06e53898a12333504350703bd

python3 Stage1_Instances/THM-M-0509/check_obligation_tree.py
  exit 0
  PASS THM-M-0509 obligation tree: 15 obligations, 40 typed edges
  registry denominator sha256: 74b4c30d82e3aa7c44f356d24eb5cd21c2d48ce06e53898a12333504350703bd
  root closure: open (M4); analytic sieve and P2-extraction packages remain open

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0509
  exit 0: rank 883, planned, theorem_complete false

cd Stage1_Instances/THM-M-0509 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0509 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_sieve_package depends on axioms: [propext]
  Statement.olean removed after the scoped check.

git diff --check -- Stage1_Instances/THM-M-0509
  exit 0; no output
```

The failed `lake env lean` invocation is retained as evidence. Lake exposes the
pinned dependency environment, but this clone has no Elan default. The retry
uses the already installed pinned Lean 4.29.0 binary and the same Lake-derived
`LEAN_PATH`; it does not alter `.lake`.

These checks validate frozen denominators, required node fields, reciprocal
proof edges, graph adjacency, acyclicity, recipe coverage, source hashes,
hygiene, elaboration, and the conditional handoff's axiom surface. They do not
prove its explicit `ChenTheoremTarget` premise. There is no accepted receipt;
master acceptance remains required.
