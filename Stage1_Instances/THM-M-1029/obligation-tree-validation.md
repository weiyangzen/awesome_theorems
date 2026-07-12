# THM-M-1029 obligation-tree validation

Item: `S56-M-1029-OBLIGATION_TREE`  
Base revision: `003528e41c522d26270c91f61e92d738221c03c8`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake dependency artifacts. No update,
build, clone, fetch, or dependency mutation ran.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1029/build_obligation_artifacts.py
  exit 0
  f5ba78d2ff64231db87b356cdf2827f4d9173387c0a387c3acfbddad19cf0fb4

python3 Stage1_Instances/THM-M-1029/check_obligation_tree.py
  exit 0
  PASS THM-M-1029 obligation tree: 14 obligations, 28 typed edges
  registry denominator sha256: f5ba78d2ff64231db87b356cdf2827f4d9173387c0a387c3acfbddad19cf0fb4
  root closure: open (M3); increment-law package remains M4

cd Formalizations/Lean &&
  lake env lean -o ../../Stage1_Instances/THM-M-1029/Statement.olean \
    ../../Stage1_Instances/THM-M-1029/Statement.lean
  exit 1
  Lean rejected an input outside the Lake package root. This invocation did
  not elaborate or write the requested olean and is retained as failed evidence.

cd Stage1_Instances/THM-M-1029 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
  exit 0
  Statement elaborated; conditional composition elaborated; `#print axioms`
  reported `[propext, Classical.choice, Quot.sound]`; temporary olean removed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1029
  exit 0: rank 222, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1029
  exit 0; no output
```

The structural validator checks frozen input hashes, the canonical denominator,
all required node fields, budgets at most 100, typed endpoints and adjacency,
reciprocal proof/composition edges, acyclicity and exact root reachability,
recipe coverage, closure boundaries, and placeholder hygiene. The Lean check
validates only the exact conditional child-to-root composition. It does not
prove `IncrementLawPackage` or Levy's theorem.

## Status boundary

This phase is self-tested pending master acceptance. The registry and graphs
are frozen, but the root remains `M3`, the minimal open cut is
`M1029-T-INCREMENTS`, and `H2`/`R4` remain unchanged. There is no accepted
receipt, audit completion, or theorem completion.
