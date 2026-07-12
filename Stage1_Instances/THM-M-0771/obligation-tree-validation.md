# THM-M-0771 obligation-tree validation

Item: `S56-M-0771-OBLIGATION_TREE`. Base revision:
`444819795285695894ff7b29af5c2419e0e000fa`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake closure and did not update, build, fetch, or clone dependencies.

```text
python3 Stage1_Instances/THM-M-0771/build_obligation_artifacts.py
  exit 0
  denominator: 55f8bb1bbc12e97eb61dd7f0551d6d8f07a0c7ec6cf4d85e692914bd700d5c61

python3 Stage1_Instances/THM-M-0771/check_obligation_tree.py
  exit 0
  PASS THM-M-0771 obligation tree: 9 obligations, 25 typed edges
  root closure: open (M3); well-order construction and release overlays remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0771
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_relationWitness has the exact WellOrderingTarget conclusion
  root_of_relationWitness and relationWitness_iff depend on no axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0771
  exit 0; rank 780, planned, theorem_complete false
git diff --check
  exit 0
```

An initial Lean attempt used a repository-style module prefix and exited 1
because the target-local compiled object is created beside the source. Using
the established local `import Statement` recipe fixed module resolution. The
successful recipe above removes its temporary object afterward.

The structural checker validates freeze hashes, the immutable denominator,
eligibility projections, node schemas and budgets, seven adjacency maps,
reciprocal proof edges, acyclic reachability, recipe coverage, the open-root
boundary, and placeholder hygiene. Lean validates only conditional composition,
so the construction leaf and theorem root remain open.
