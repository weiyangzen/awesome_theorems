# THM-M-0986 obligation-tree validation

Item: `S56-M-0986-OBLIGATION_TREE`  
Base revision: `aa8a8afff8eb3496c9223c57b562cceb553f8a74`  
Validation date: 2026-07-12

The worker reused the canonical pinned Lake artifacts through the pre-existing
untracked `Formalizations/Lean/.lake` link. No update, build, clone, fetch, or
dependency mutation ran; this is nonrelease worker evidence.

## Commands and results

```text
python3 Stage1_Instances/THM-M-0986/build_obligation_artifacts.py
  exit 0
  7051508e4dd19f51c8eba3519376d3f60514dbec784f028a50b748d7ec8d6dec

python3 Stage1_Instances/THM-M-0986/check_obligation_tree.py
  exit 0
  PASS THM-M-0986 obligation tree: 11 obligations, 20 typed edges
  root closure: open (M3); strong-law and average-measurability packages remain unaccepted

cd Stage1_Instances/THM-M-0986 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
  exit 0
  statement and conditional composition elaborated; `#print axioms` reported
  `[propext, Classical.choice, Quot.sound]`; temporary olean removed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-0986
  exit 0: rank 266, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
rg -n '\bsorry\b|\baxiom\b|\badmit\b|sorryAx'
  Stage1_Instances/THM-M-0986 --glob '*.lean'
  exit 1: no forbidden Lean declarations or placeholders
git diff --check -- Stage1_Instances/THM-M-0986 .stage1-worker-selftest.json
  exit 0; no output
```

The structural validator checks frozen input hashes, canonical denominators,
all required node fields, budgets no greater than 100, typed endpoints and
adjacency, reciprocal proof/composition edges, proof-DAG acyclicity and exact
reachability, validation-recipe coverage, closure boundaries, and placeholder
hygiene. Lean validates only the exact conditional child-to-root composition.

## Status boundary

This phase is self-tested pending master acceptance. The registry and typed
graphs are frozen, but the root remains `M3`; the minimal open cut contains the
strong-law and average-measurability packages. Candidate discovery does not
promote either package. No receipt, audit completion, or theorem completion is
claimed.
