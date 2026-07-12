# THM-M-1016 obligation-tree validation

Item: `S56-M-1016-OBLIGATION_TREE`  
Base revision: `3988dde7b18619a1cac9d1022256785302545497`  
Validation date: 2026-07-12

The worker reused the materialized pinned Lake artifacts. It did not run an update, build, clone,
fetch, or any dependency mutation.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1016/build_obligation_artifacts.py
  exit 0
  a0552dc7b546e055218200f066ebeb2cce448a60ac46a162949c1a57647fcef4

python3 Stage1_Instances/THM-M-1016/check_obligation_tree.py
  exit 0
  PASS THM-M-1016 obligation tree: 14 obligations, 32 typed edges
  registry denominator sha256: a0552dc7b546e055218200f066ebeb2cce448a60ac46a162949c1a57647fcef4
  root closure: open (M3); scaled Frechet remainder remains M4

LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  -o Stage1_Instances/THM-M-1016/Statement.olean \
  Stage1_Instances/THM-M-1016/Statement.lean
LEAN_PATH=Stage1_Instances/THM-M-1016:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
  Stage1_Instances/THM-M-1016/ObligationTree.lean
  combined exit 0
  Statement elaborated with pre-existing unused-variable warnings.
  Conditional composition elaborated; #print axioms reported
  [propext, Classical.choice, Quot.sound]. Temporary Statement.olean removed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1016
  exit 0: rank 295, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json, validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1016
  exit 0; no output
```

The structural validator checks frozen input hashes, denominator projections, all node fields,
budgets at most 100, typed endpoints and adjacency, reciprocal proof/composition edges, acyclicity,
recipe coverage, the open closure boundary, and placeholder hygiene. The Lean check proves only the
explicit child-to-conclusion composition and does not supply the Frechet remainder premise.

## Status boundary

This phase is self-tested pending master acceptance. The registry and typed graphs are frozen, but
the root remains `H2/M3/R4`; the minimal open cut is `M1016-T-REMAINDER`. No accepted receipt,
audit completion, or theorem completion is claimed.
