# THM-M-0557 obligation-tree validation

Item: `S56-M-0557-OBLIGATION_TREE`. Base revision:
`be98a856ad5cbf322fb2fda71f1506bd05f1d355`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake environment and did not update, build, clone, or fetch dependencies.

```text
python3 Stage1_Instances/THM-M-0557/build_obligation_artifacts.py
  exit 0
  wrote 9 obligations and 49 typed edges
  6e74b519b624746e5ccc8e7e1d58762390de75915589e808dd9da94d79908596

python3 Stage1_Instances/THM-M-0557/check_obligation_tree.py
  exit 0
  PASS THM-M-0557 obligation tree: 9 obligations, 49 typed edges
  registry denominator sha256: 6e74b519b624746e5ccc8e7e1d58762390de75915589e808dd9da94d79908596
  root closure: open (M3); group and commutative integration remain proof-node work

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0557/ObligationTree.lean
  exit 0
  all six pinned route declarations resolved
  exactTarget_of_branches depends on [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0557
  exit 0; rank 605, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json, and
obligation-tree-receipt.json
  exit 0 for all three files
git diff --check -- Stage1_Instances/THM-M-0557 .stage1-worker-selftest.json
  exit 0; no output
```

The structural validator recomputes the frozen denominator, pins the statement
and anchor-audit byte hashes, checks all required node ledgers and 100-step
ceilings, validates typed adjacency and reciprocal proof edges, proves DAG
reachability, and enforces the fail-closed root boundary. The Lean check proves
only conditional child-to-parent composition. It does not discharge either
remaining branch or establish H0, M0, R0, audit completion, validation/release,
or theorem completion. Master acceptance remains required.
