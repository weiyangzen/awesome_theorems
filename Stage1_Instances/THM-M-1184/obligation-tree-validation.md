# THM-M-1184 obligation-tree validation

Item: `S56-M-1184-OBLIGATION_TREE`. Base revision:
`3cb5c69018ebf704c6fd68f32aaece780d6bf542`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts and installed Lean 4.29.0 toolchain. It did not update,
fetch, clone, or otherwise mutate dependencies.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
  slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1184
  exit 0
  rank 169; lane hard_mathlib_anchor_and_wrapper; lifecycle planned;
  theorem_complete false

python3 Stage1_Instances/THM-M-1184/build_obligation_artifacts.py
  exit 0
  4626bc02bb751442b67f842fd1e77a79210940bdd405134d5b14c41f1ff07e27

python3 Stage1_Instances/THM-M-1184/check_obligation_tree.py
  exit 0
  PASS THM-M-1184 obligation tree: 16 obligations, 43 typed edges
  registry denominator sha256:
    4626bc02bb751442b67f842fd1e77a79210940bdd405134d5b14c41f1ff07e27
  root closure: open (M2); weak and reverse duality packages remain open

cd Formalizations/Lean &&
  lake env lean -R ../../Stage1_Instances/THM-M-1184
    ../../Stage1_Instances/THM-M-1184/Statement.lean
    -o ../../Stage1_Instances/THM-M-1184/Statement.olean &&
  LEAN_PATH=../../Stage1_Instances/THM-M-1184:$(lake env printenv LEAN_PATH)
    lake env lean -R ../../Stage1_Instances/THM-M-1184
      ../../Stage1_Instances/THM-M-1184/ObligationTree.lean
  exit 0
  root_of_duality_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  The scoped Statement.olean was removed after validation.

git diff --check -- Stage1_Instances/THM-M-1184 .stage1-worker-selftest.json
  exit 0; no output
```

The checks bind the registry to the exact statement and anchor-audit hashes,
recompute the frozen denominator, enforce unique and reciprocal typed edges,
check proof-DAG reachability and acyclicity, enforce leaf budgets, reject Lean
placeholder tokens, and kernel-elaborate the exact conditional composition.
They do not prove weak duality, reverse duality, or the canonical root. There
is no accepted receipt; master acceptance remains required.
