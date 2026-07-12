# THM-M-0786 obligation-tree validation

Item: `S56-M-0786-OBLIGATION_TREE`  
Base revision: `5278269d3ea693eba5c4c533ad3fe61693da0620`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

Existing canonical pinned Lake artifacts were reused. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

## Commands and results

```text
python3 Stage1_Instances/THM-M-0786/build_obligation_artifacts.py
  exit 0
  388471796332e9e00b2f291ca80ee0b57ecc8ab3880868fd329ea2b2270d71c3

python3 Stage1_Instances/THM-M-0786/check_obligation_tree.py
  exit 0
  PASS THM-M-0786 obligation tree: 14 obligations, 44 typed edges
  registry denominator sha256: 388471796332e9e00b2f291ca80ee0b57ecc8ab3880868fd329ea2b2270d71c3
  root closure: open (M3); external kernel integration and canonical adapter remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0786
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  canonical BorelDeterminacyTarget type printed
  root_of_payoffSolver depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets with ranks 1..1546 passed

python3 scripts/stage1_target.py show THM-M-0786
  exit 0; rank 791, planned, L0/rework-required, theorem_complete false
```

The generator freezes source hashes, eligibility denominators, 14 semantic
ledgers, six separately typed graph surfaces, and per-node validation recipes.
The checker validates hashes, uniqueness, denominator projections, budgets,
adjacency, reciprocal proof edges, acyclicity, recipe coverage, and placeholder
hygiene. Lean validates only the exact statement and conditional final
composition. It does not validate the external theorem, adapter, primary-source
map, trust closure, or theorem completion. Master acceptance remains required.
