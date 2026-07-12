# THM-M-1024 obligation-tree validation

Item: `S56-M-1024-OBLIGATION_TREE`  
Base revision: `45aefb41a1978e4156e78f7fe59c590530703225`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake dependency artifacts. No update, build, clone, fetch, or
dependency mutation ran. The pre-existing untracked `Formalizations/Lean/.lake` symlink exposes the
canonical pinned artifacts and was not modified.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1024/build_obligation_artifacts.py
  exit 0
  09ae507f5852e0e927272c16a31701c7b4e7a9f69359716285d2a915bdb44921

python3 Stage1_Instances/THM-M-1024/check_obligation_tree.py
  exit 0
  PASS THM-M-1024 obligation tree: 24 obligations, 66 typed edges
  registry denominator sha256: 09ae507f5852e0e927272c16a31701c7b4e7a9f69359716285d2a915bdb44921
  root closure: open (M3); forward, converse, and uniqueness packages remain M4

LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  -o Stage1_Instances/THM-M-1024/Statement.olean \
  Stage1_Instances/THM-M-1024/Statement.lean
LEAN_PATH=Stage1_Instances/THM-M-1024:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  Stage1_Instances/THM-M-1024/ObligationTree.lean
  combined exit 0
  Statement elaborated and conditional composition elaborated.
  #print axioms root_of_packages reported [propext, Classical.choice, Quot.sound].
  The temporary Statement.olean was removed.

python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1024
  exit 0: rank 500, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1024 .stage1-worker-selftest.json
  exit 0; no output
```

The structural validator checks frozen input hashes, the canonical denominator, eligibility
projections, required node fields, budgets at most 100, typed endpoints and adjacency, reciprocal
proof/composition edges, proof-graph acyclicity and exact root reachability, structured recipe
shape and coverage, the three-node root cut, and placeholder hygiene. The Lean check validates only
the exact conditional child-to-root composition. It does not prove any of the three packages.

## Status boundary

This phase is self-tested pending master acceptance. The registry and typed graphs are frozen, but
the root remains `M3`; forward, converse, and uniqueness remain `M4`; and `H1`/`R3` remain
unchanged. There is no accepted receipt, audit completion, or theorem completion.
