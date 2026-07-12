# THM-M-1041 obligation-tree validation

Item: `S56-M-1041-OBLIGATION_TREE`  
Base revision: `8b61d0242da6b4b6810daf423a82881bc4a5c956`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake dependency artifacts. No update,
build, clone, fetch, or dependency mutation ran.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1041/build_obligation_artifacts.py
  exit 0
  b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42

python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py
  exit 0
  PASS THM-M-1041 obligation tree: 21 obligations, 56 typed edges
  registry denominator sha256:
  b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42
  root closure: open (M4); forward and converse packages remain M4

cd Stage1_Instances/THM-M-1041 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
  exit 0
  Statement and conditional composition elaborated; `#print axioms` reported
  `[propext, Classical.choice, Quot.sound]`; temporary olean removed.

python3 Stage1_Instances/THM-M-1041/check_statement.py
  exit 0; exact expression fingerprint unchanged and three mutations killed
python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py
  exit 0; anchor audit invariants pass
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-1041
  exit 0; rank 234, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json
  exit 0 for all three
git diff --check -- Stage1_Instances/THM-M-1041
  exit 0; no output
```

The structural validator checks frozen input hashes, the canonical denominator,
all required node fields, budgets at most 100, typed endpoints and adjacency,
reciprocal proof/composition edges, acyclicity and exact proof-node
reachability, recipe coverage, closure boundaries, and placeholder hygiene.
The Lean check validates only the exact conditional child-to-root composition.
It does not inhabit either direction package or prove Hille--Yosida.

## Status boundary

This phase is self-tested pending master acceptance. The registry and graphs
are frozen, but the root remains `M4`, the minimal open cut is
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`, and `H2`/`R4` remain unchanged. There
is no accepted receipt, audit completion, or theorem completion.
