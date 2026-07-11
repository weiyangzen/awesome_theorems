# THM-M-0579 obligation-tree validation

Item: `S56-M-0579-OBLIGATION_TREE`. Base revision:
`f104b8226edf6943aeb5d45a2b8b5a202bb3b8dc`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, build, clone, or fetch was run.

```text
python3 Stage1_Instances/THM-M-0579/build_obligation_artifacts.py
  exit 0
  984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f

python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py
  exit 0
  PASS THM-M-0579 obligation tree: 16 obligations, 34 typed edges
  registry denominator sha256: 984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f
  root closure: open (M3); recognition and rigidity packages remain M4

cd Stage1_Instances/THM-M-0579 &&
  LEAN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" ObligationTree.lean
  exit 0
  root_of_recognition_and_rigidity depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0579
  exit 0: rank 114, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0579
  exit 0; no output
```

This validates input hashes, frozen denominators, required node ledgers, typed
reciprocal proof edges, adjacency, proof-DAG reachability, validation-recipe
coverage, placeholder hygiene, elaboration, exact output type, and the checked
conditional composition's axiom surface. It does not prove either package
premise. There is no accepted receipt; master acceptance remains required.
