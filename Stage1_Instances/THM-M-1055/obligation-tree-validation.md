# THM-M-1055 obligation-tree validation

Item: `S56-M-1055-OBLIGATION_TREE`  
Base revision: `42186a75d7cd08ea38daa2739e6cb8a34b59dc49`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake dependency artifacts. No update,
build, clone, fetch, or dependency mutation ran. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not changed by this phase.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1055/build_obligation_artifacts.py
  exit 0
  cb67895834a856b780f44cbcf8c3de106f574f5035d3003486181876fd382d06

python3 Stage1_Instances/THM-M-1055/check_obligation_tree.py
  exit 0
  PASS THM-M-1055 obligation tree: 14 obligations, 30 typed edges
  registry denominator sha256: cb67895834a856b780f44cbcf8c3de106f574f5035d3003486181876fd382d06
  root closure: open (M3); invariant-limit package remains M4

LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  -o Stage1_Instances/THM-M-1055/Statement.olean \
  Stage1_Instances/THM-M-1055/Statement.lean &&
LEAN_PATH=Stage1_Instances/THM-M-1055:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  Stage1_Instances/THM-M-1055/ObligationTree.lean
  exit 0
  The exact statement and conditional composition elaborated. `#print axioms`
  reported `[propext, Classical.choice, Quot.sound]`. The temporary
  `Statement.olean` was removed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1055
  exit 0: rank 247, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1055
  exit 0; no output
```

The structural validator checks frozen input hashes, the canonical denominator,
required node fields, budgets at most 100, typed endpoints and adjacency,
reciprocal proof/composition edges, acyclicity and exact root reachability,
structured recipe coverage, closure boundaries, and placeholder hygiene. Lean
validates only the exact child-to-root conditional composition; it does not
prove `InvariantLimitPackage` or the Birkhoff theorem.

## Status boundary

This phase is self-tested pending master acceptance. The root remains `M3`,
the minimal open cut is `M1055-T-INVARIANT-LIMIT`, and `H2`/`R4` remain
unchanged. There is no accepted receipt, audit completion, or theorem
completion.
