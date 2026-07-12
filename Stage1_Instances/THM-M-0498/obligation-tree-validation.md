# THM-M-0498 obligation-tree validation

Item: `S56-M-0498-OBLIGATION_TREE`. Base revision:
`acfb5cdfcf75eadcf18e7f322e4fc4097c3e0077`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No update, build, fetch, clone, or dependency mutation
was performed.

```text
python3 Stage1_Instances/THM-M-0498/build_obligation_artifacts.py
  exit 0
  8a964cd4c13dc98d9bfa75e22cf5bab2af31d96d83bde13600049c669d88f144

python3 Stage1_Instances/THM-M-0498/check_obligation_tree.py
  exit 0
  PASS THM-M-0498 obligation tree: 15 obligations, 33 typed edges
  registry denominator sha256: 8a964cd4c13dc98d9bfa75e22cf5bab2af31d96d83bde13600049c669d88f144
  root closure: open (M4); analytic explicit-formula package remains M4

cd Stage1_Instances/THM-M-0498 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0498 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_analytic_package depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 -m py_compile Stage1_Instances/THM-M-0498/build_obligation_artifacts.py \
  Stage1_Instances/THM-M-0498/check_obligation_tree.py
  exit 0
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0498
  exit 0: rank 258, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0498
  exit 0; no output
```

The failed `lake env lean` command is retained as a known environment failure:
Lake reads the pinned dependency environment, but this clone has no configured
Elan default. The successful retry uses the already installed pinned Lean
4.29.0 executable with the same Lake-derived `LEAN_PATH`.

The checks cover input hashes, the frozen denominator, eligibility and
exclusion sets, required node ledgers, all seven typed graphs, reciprocal proof
edges, graph adjacency, proof-DAG acyclicity and reachability, structured recipe
coverage, placeholder hygiene, elaboration, exact-root conditional composition,
and its axiom surface. They do not prove the open analytic package. There is no
accepted receipt; master acceptance remains required.
