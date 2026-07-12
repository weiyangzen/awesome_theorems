# THM-M-0468 obligation-tree validation

Item: `S56-M-0468-OBLIGATION_TREE`. Base revision:
`540de1f8d50dd82b5695b80f6568f470b21233a4`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No dependency update, build, clone, fetch, or `.lake`
mutation was performed.

## Commands and results

```text
python3 Stage1_Instances/THM-M-0468/build_obligation_artifacts.py
  exit 0
  wrote 20 obligations and 44 typed edges
  0b32411582135d1a69e072b6f099b06525943e09f95e27938808e9edcd5968c4

python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py
  exit 0
  PASS THM-M-0468 obligation tree: 20 obligations, 44 typed edges
  registry denominator sha256:
    0b32411582135d1a69e072b6f099b06525943e09f95e27938808e9edcd5968c4
  root closure: open (M4); forward and converse packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0468/Statement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-0468/ObligationTree.lean
  exit 1
  Statement.lean elaborated; ObligationTree.lean could not resolve the local
  Statement module because no local olean was on that invocation's search path.

cd Stage1_Instances/THM-M-0468 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) \
      ObligationTree.lean
  exit 0
  root_of_direction_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0468
  exit 0; rank 314, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0468/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file
git diff --check -- Stage1_Instances/THM-M-0468 .stage1-worker-selftest.json
  exit 0; no output
```

The failed first local-import attempt is retained rather than hidden. The
successful narrow retry uses `lake env which lean` and the Lake-derived pinned
dependency path, then deletes its temporary olean.

These checks validate the frozen denominator, required node schema, step
budgets, graph separation and adjacency, reciprocal proof/composition edges,
proof-DAG acyclicity and reachability, structured recipe coverage, placeholder
hygiene, elaboration, and exact conditional composition. The Lean axiom output
records only the imported foundation surface of the conditional theorem; it
does not close either premise. The immediate root cut remains the forward and
converse packages. No audit or theorem completion is claimed, and master
acceptance is still required.
