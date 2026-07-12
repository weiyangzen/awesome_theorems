# THM-M-1108 obligation-tree validation

Item: `S56-M-1108-OBLIGATION_TREE`. Base revision:
`4b371df18255c744c75b2aa9dbfaa4ebfd983dbf`.

Validation ran from the worker clone on 2026-07-12 using the existing pinned
Lake artifacts. No dependency update, build, fetch, or clone was run.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1108/build_obligation_artifacts.py
  exit 0
  generated 18 obligations; denominator
  2defff919b6296d9507f9769f1da7ba4bbeea305768a4df8fff8373aa0322c8e

python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py
  exit 0
  PASS THM-M-1108 obligation tree: 18 obligations, 36 typed edges
  registry denominator sha256:
  2defff919b6296d9507f9769f1da7ba4bbeea305768a4df8fff8373aa0322c8e
  root closure: open (M3); Poissonized and de-Poissonization packages remain M4

cd Formalizations/Lean &&
  lake env lean -o ../../Stage1_Instances/THM-M-1108/Statement.olean \
    ../../Stage1_Instances/THM-M-1108/Statement.lean
  exit 1
  input file must be contained in root directory Formalizations/Lean

cd Formalizations/Lean &&
  lake env lean --root=../.. \
    -o ../../Stage1_Instances/THM-M-1108/Statement.olean \
    ../../Stage1_Instances/THM-M-1108/Statement.lean &&
  LEAN_PATH=../../Stage1_Instances/THM-M-1108:$(lake env printenv LEAN_PATH) \
    lake env lean --root=../.. \
      ../../Stage1_Instances/THM-M-1108/ObligationTree.lean
  exit 0
  canonicalStatement_of_poissonized_depoissonized depends on axioms:
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-1108
  exit 0; rank 548, planned, L0/rework_required, theorem incomplete
python3 -m json.tool Stage1_Instances/THM-M-1108/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1108/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1108/validation-specs.json
  each exit 0
git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json
  exit 0; no output
```

The first Lean attempt is retained as evidence of a command-shape error. The
successful retry supplies the worker root explicitly, uses `lake env lean` and
the pinned Lake-derived `LEAN_PATH`, and removes the temporary `Statement.olean`
afterward. Lean elaborated the exact child interfaces and composition theorem.
The axiom output is the expected foundation surface inherited through the
definitions; it includes no custom axiom or oracle.

The structural checker validates frozen input hashes and denominator hash,
node schema and step budgets, typed graph adjacency and reciprocal proof
edges, root reachability, DAG acyclicity, validation-recipe coverage, source
hygiene, and the explicit open-root boundary. This is nonrelease evidence. The
two mathematical packages remain unproved, and master acceptance is required.
