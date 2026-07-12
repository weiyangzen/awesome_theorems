# THM-M-0983 obligation-tree validation

Item: `S56-M-0983-OBLIGATION_TREE`. Base revision:
`b464f991efe5978f547092d80ac4bce99d6485c3`.

Validation ran from the worker clone on 2026-07-12. It reused the existing pinned Lake artifacts;
no dependency update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0983/build_obligation_artifacts.py
  exit 0
  ce70278bd094af1d59933621976c0a1a80fbeadc8f867f58d855ea0048006be4

python3 Stage1_Instances/THM-M-0983/check_obligation_tree.py
  exit 0
  PASS THM-M-0983 obligation tree: 10 obligations, 32 typed edges
  registry denominator sha256: ce70278bd094af1d59933621976c0a1a80fbeadc8f867f58d855ea0048006be4
  root closure: open (M3); three explicit package premises remain downstream

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0983/ObligationTree.lean
  exit 0
  root_of_packages depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0983
  exit 0: rank 263, planned, theorem_complete false
python3 -m json.tool <each changed JSON file>
  exit 0 for obligation-registry.json, typed-graphs.json, validation-specs.json, and intake.json
git diff --check -- Stage1_Instances/THM-M-0983
  exit 0; no output
```

The checks cover frozen-input and denominator hashes, complete required node fields, graph endpoint
types and adjacency, reciprocal proof edges, acyclic root reachability, per-node validation recipes,
forbidden proof placeholders, conditional composition elaboration, and its axiom surface. They do
not discharge the three explicit package premises. There is no accepted receipt; master acceptance
and every downstream proof/release gate remain required.
