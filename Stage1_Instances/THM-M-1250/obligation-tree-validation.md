# THM-M-1250 obligation-tree validation

Item: `S56-M-1250-OBLIGATION_TREE`. Base revision:
`58cde546113e54bfa95299c69db6ee1508316872`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or `.lake` mutation ran.

```text
python3 Stage1_Instances/THM-M-1250/build_obligation_artifacts.py
  exit 0
  generated 15 obligations; denominator
  24c4c3e89df76e28bfa658401de1edd90d5000ad1897f89d2495a071bb098bca

python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py
  exit 0
  PASS THM-M-1250 obligation tree: 15 obligations, 30 typed edges
  registry denominator sha256: 24c4c3e89df76e28bfa658401de1edd90d5000ad1897f89d2495a071bb098bca
  root closure: open (M3); forward and reverse packages remain explicit

cd Formalizations/Lean &&
  BASE_LEAN_PATH=$(lake env printenv LEAN_PATH) &&
  cd ../../Stage1_Instances/THM-M-1250 &&
  LEAN_PATH="$BASE_LEAN_PATH" lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=".:$BASE_LEAN_PATH" lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

Same scoped command with the exact pinned executable
/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
  exit 0
  characterization_of_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the check

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1250
  exit 0: rank 430, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1250 .stage1-worker-selftest.json
  exit 0; no output
```

The failed direct `lake env lean` attempt is retained as evidence. Lake exposes
the pinned dependency path, but this clone has no Elan default. The successful
retry uses the already-installed Lean 4.29.0 executable and that same
Lake-derived `LEAN_PATH`.

The checks cover content hashes, denominators, node ledgers, typed adjacency,
reciprocal proof edges, acyclicity, root reachability, placeholder hygiene,
Lean elaboration, exact conditional root composition, and its axiom surface.
They do not prove either explicit direction package. No accepted receipt exists;
master acceptance remains required.
