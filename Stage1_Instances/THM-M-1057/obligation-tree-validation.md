# THM-M-1057 obligation-tree validation

Item: `S56-M-1057-OBLIGATION_TREE`  
Base revision: `ff4e83f798358bf80798541f0b3f627121e1e617`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake artifacts. No update, build, clone,
fetch, or dependency mutation ran. The pre-existing untracked
`Formalizations/Lean/.lake` link is unrelated worker-clone infrastructure, so
this is nonrelease evidence.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1057/build_obligation_artifacts.py
  exit 0
  080ff4e9ec6298847c52b7135ca47d9d57aecd0797d2ff1acd6161aaf1b0f67c

python3 Stage1_Instances/THM-M-1057/check_obligation_tree.py
  exit 0
  PASS THM-M-1057 obligation tree: 15 obligations, 46 typed edges
  registry denominator sha256: 080ff4e9ec6298847c52b7135ca47d9d57aecd0797d2ff1acd6161aaf1b0f67c
  root closure: open (M3); pointwise-limit package remains M4

LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1057
LEAN_PATH="$LEAN_PATH" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=.:"$LEAN_PATH" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  Statement and conditional composition elaborated. `#print axioms` reported
  `[propext, Classical.choice, Quot.sound]`; no `sorryAx` was present.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1057
  exit 0: rank 249, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1057
  exit 0; no output
```

The structural validator checks the frozen input hashes, canonical denominator,
all required node fields, budgets at most 100, typed endpoints and adjacency,
reciprocal proof/composition edges, proof-DAG acyclicity and exact root
reachability, recipe coverage, closure boundaries, and placeholder hygiene.

## Status boundary

This phase is self-tested pending master acceptance. The root remains `M3`, the
minimal open cut is `M1057-T-LIMIT-PACKAGE`, and `[H1, R3]` debt is unchanged.
There is no accepted receipt, audit completion, or theorem completion.
