# THM-M-0586 obligation-tree validation

Item: `S56-M-0586-OBLIGATION_TREE`  
Base revision: `921c8426cee302d0d5c6cd7fe2037c94db1db75f`  
Validation date: 2026-07-12

The existing pinned Lake artifacts were reused. No dependency update, build, clone, or fetch was
performed.

```text
python3 Stage1_Instances/THM-M-0586/build_obligation_artifacts.py
  exit 0
  bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e

python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py
  exit 0
  PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges
  registry denominator sha256: bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e
  root closure: open (M3); dimension-five and stable-dimension packages remain M4

cd Formalizations/Lean
LEAN=$(lake env which lean); LP=$(lake env printenv LEAN_PATH)
cd ../../Stage1_Instances/THM-M-0586
LEAN_PATH="$LP" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LP" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  highDimensionalPoincare_of_dimension_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0586
  exit 0: rank 117, planned, L0/rework-required, theorem incomplete

git diff --check -- Stage1_Instances/THM-M-0586
  exit 0; no output
```

The validator recomputes input and denominator hashes, checks every required registry and node
field, frozen eligibility projections, graph endpoint and adjacency integrity, reciprocal proof
edges, proof-DAG acyclicity and root reachability, validation-recipe coverage, hygiene, and the
explicit open closure boundary. Lean kernel-checks only the exhaustive recomposition from the two
named package premises. The ordinary mathlib axiom surface shown above is recorded, not treated as
a proof of either premise.

The root remains open. There is no accepted receipt, full source-node crosswalk, proof of the
dimension-five package, proof of the stable package, audit completion, or theorem completion.
