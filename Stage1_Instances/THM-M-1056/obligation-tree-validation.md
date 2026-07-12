# THM-M-1056 obligation-tree validation

Item: `S56-M-1056-OBLIGATION_TREE`  
Base revision: `e57019f939f278f5d98bf089d747af310e0a6b58`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake artifacts. It did not run Lake
update/build, fetch, clone, or any dependency mutation. The pre-existing
untracked `Formalizations/Lean/.lake` link/artifact is outside this item's owned
path and was not changed.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1056/build_obligation_artifacts.py
  exit 0
  5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828

python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py
  exit 0
  PASS THM-M-1056 obligation tree: 19 obligations, 49 typed edges
  registry denominator sha256:
    5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828
  root closure: open (M3); Oseledets core package remains M4

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_VALUE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1056
LEAN_PATH="$LEAN_PATH_VALUE" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH_VALUE" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  Exact statement and conditional composition elaborated. `#print axioms`
  reported `[propext, Classical.choice, Quot.sound]`. Existing unused-binder
  linter warnings were emitted for statement parameters and the matching
  conditional package. The temporary olean was removed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1056
  exit 0: rank 248, planned, legacy artifacts unaccepted, theorem incomplete
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1056
  exit 0; no output
```

The structural validator checks frozen input hashes, canonical denominators,
all required node fields, leaf budgets at most 100, typed endpoints and
adjacency, reciprocal proof/composition edges, proof-DAG acyclicity and exact
root reachability, validation recipe coverage, explicit open closure, and
placeholder hygiene. Lean validates only the exact conditional child-to-root
composition. It does not prove `OseledetsCorePackage` or Oseledets' theorem.

## Status boundary

This phase is self-tested pending master acceptance. The frozen minimal open
root cut is `M1056-T-CORE`; the root remains `M3`, while source acceptance,
readability review, provenance closure, audit completion, theorem completion,
and an accepted receipt remain open.
