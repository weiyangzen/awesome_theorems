# THM-M-1008 obligation-tree validation

Item: `S56-M-1008-OBLIGATION_TREE`. Base revision:
`11ec0ea4b441f1e6bc5580ca9a037509892e8c92`.

Validation ran from the worker clone on 2026-07-12. The existing pinned Lake artifacts were reused;
no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1008/build_obligation_artifacts.py
  exit 0
  d41339ef9ffeddf215d8f5f37732901fbfecdb1b1f662e794344c7a2f4665b3d

python3 Stage1_Instances/THM-M-1008/check_obligation_tree.py
  exit 0
  PASS THM-M-1008 obligation tree: 15 obligations, 30 typed edges
  registry denominator sha256: d41339ef9ffeddf215d8f5f37732901fbfecdb1b1f662e794344c7a2f4665b3d
  root closure: open (M2); self-independence package remains M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1008/ObligationTree.lean
  exit 1
  unknown module prefix 'Statement'

BASE_LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env printenv LEAN)
cd Stage1_Instances/THM-M-1008
LEAN_PATH=$BASE_LEAN_PATH $LEAN -o Statement.olean Statement.lean
LEAN_PATH=.:$BASE_LEAN_PATH $LEAN ObligationTree.lean
rm -f Statement.olean
  exit 0
  zeroOne_of_selfIndependence depends on axioms:
    [propext, Classical.choice, Quot.sound]
  root_of_selfIndependencePackage depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1008
  exit 0: rank 288, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-1008/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file
git diff --check -- Stage1_Instances/THM-M-1008 .stage1-worker-selftest.json
  exit 0; no output
```

The direct Lean invocation failed because an owned sibling module is not on the default Lake module
path; it is recorded rather than hidden. The successful scoped recipe first elaborates
`Statement.lean` to a temporary `Statement.olean`, then uses the exact pinned Lean executable and
Lake-derived dependency path. The temporary object is removed afterward.

These checks validate source-bound registry hashes, frozen denominators, node ledgers, distinct
typed graphs, reciprocal proof/composition edges, graph adjacency, proof-DAG reachability, recipe
coverage, hygiene, the pinned self-independence endpoint, and conditional exact-root composition.
They do not prove the explicit `SelfIndependencePackage` premise. There is no accepted receipt;
master acceptance remains required, and theorem completion remains false.
