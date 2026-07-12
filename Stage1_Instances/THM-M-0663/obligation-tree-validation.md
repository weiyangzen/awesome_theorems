# THM-M-0663 obligation-tree validation

Item: `S56-M-0663-OBLIGATION_TREE`. Base revision:
`c62c7e6f4b9f2eace4ef9d3f7e3e90240c96391f`. Validation ran in the worker
clone on 2026-07-12. Existing pinned Lake artifacts were reused; no update,
build, dependency fetch, or dependency clone was run.

```text
python3 Stage1_Instances/THM-M-0663/build_obligation_artifacts.py
  exit 0
  0e54d5483488181af11d415bb6e29860b351fce14b297a02bd45d9ee269faf53

python3 Stage1_Instances/THM-M-0663/check_obligation_tree.py
  exit 0
  PASS THM-M-0663 obligation tree: 14 obligations, 36 typed edges
  registry denominator sha256: 0e54d5483488181af11d415bb6e29860b351fce14b297a02bd45d9ee269faf53
  root closure: open (M3); local behavior, finiteness, source, and foundation packages remain open

python3 -m json.tool Stage1_Instances/THM-M-0663/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0663
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_partition_package depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0663
  exit 0; rank 707, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0663 .stage1-worker-selftest.json
  exit 0; no output
```

The structural checker validates the two freeze hashes, immutable denominator,
eligibility projections, node completeness, typed adjacency, reciprocal proof
edges, proof-graph acyclicity, validation-recipe coverage, and placeholder
hygiene. Lean checks the exact proposition and conditional root interface. The
reported axioms arise from elaborating the proposition's mathlib definitions;
the conditional identity theorem introduces no assumed theorem declaration.

This phase freezes architecture only. It does not prove the partition package,
close the root, establish H0, or supply audit/theorem completion. Master
acceptance remains required.
