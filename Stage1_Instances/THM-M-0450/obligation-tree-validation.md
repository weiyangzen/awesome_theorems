# THM-M-0450 obligation-tree validation

Item: `S56-M-0450-OBLIGATION_TREE`. Base revision:
`68718ee926988aef75348ccb82fe2a57f88e2b44`.

Validation ran from the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts through the clone's pre-existing untracked `.lake`
symlink. No dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0450/build_obligation_artifacts.py
  exit 0
  72f2ac93d10c6e4c5b106c189ee5823c50970d512e054fb247b6796ad00d8e24

python3 Stage1_Instances/THM-M-0450/check_obligation_tree.py
  exit 0
  PASS THM-M-0450 obligation tree: 14 obligations, 31 typed edges
  registry denominator sha256: 72f2ac93d10c6e4c5b106c189ee5823c50970d512e054fb247b6796ad00d8e24
  root closure: open (M3); weak Mordell-Weil and elliptic-height packages remain open

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0450/ObligationTree.lean
  exit 0
  root_of_descent_packages has the expected two package arguments and ExactTarget result
  axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0450
  exit 0: rank 92, planned, L0/rework-required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0450/obligation-registry.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0450/typed-graphs.json >/dev/null
  both exit 0

git diff --check -- Stage1_Instances/THM-M-0450
  exit 0; no output
```

The structural check recomputes statement and anchor-audit hashes, the
eligibility projection and frozen denominator, all three eligibility lists,
unique node and edge IDs, typed graph families, adjacency, proof-DAG acyclicity
and root reachability, step budgets, Lean hygiene, and the fail-closed root
status. Lean checks the conditional composition against pinned mathlib and
shows no `sorryAx` dependency.

This validates the architecture only. The weak Mordell-Weil and height-package
arguments are explicit and uninhabited, model transport and source/provenance/
trust review remain open, and there is no accepted receipt, audit completion,
root proof, or theorem-completion claim. Master acceptance remains required.
