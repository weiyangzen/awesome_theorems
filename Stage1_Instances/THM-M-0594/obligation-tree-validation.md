# THM-M-0594 obligation-tree validation

Item: `S56-M-0594-OBLIGATION_TREE`. Base revision:
`46ae82675e83fbd3605819f1c3a6d6fb2e7328cd`. Validation date: 2026-07-12.

The worker reused the canonical pinned Lake artifacts read-only. No update,
build, dependency fetch, clone, or modification under `.lake` was performed.

```text
python3 Stage1_Instances/THM-M-0594/build_obligation_artifacts.py
  exit 0
  0ad656eddf1e42c8f47912729ceddcab9e45d56fd8a68e24b7bc82d59d367443

python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py
  exit 0
  PASS THM-M-0594 obligation tree: 16 obligations, 46 typed edges
  registry denominator sha256: 0ad656eddf1e42c8f47912729ceddcab9e45d56fd8a68e24b7bc82d59d367443
  root closure: open (M3); noncompact construction and topological bridge remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0594/ObligationTree.lean
  exit 1 (expected setup correction)
  unknown module prefix 'Statement'

cd Formalizations/Lean &&
  lake env lean -R ../../Stage1_Instances/THM-M-0594 \
    -o ../../Stage1_Instances/THM-M-0594/Statement.olean \
    ../../Stage1_Instances/THM-M-0594/Statement.lean &&
  LEAN_PATH="$(pwd)/../../Stage1_Instances/THM-M-0594:${LEAN_PATH:-}" \
    lake env lean -R ../../Stage1_Instances/THM-M-0594 \
      ../../Stage1_Instances/THM-M-0594/ObligationTree.lean
  exit 0
  root_of_smooth_embedding_witness depends on axioms:
    [propext, Classical.choice, Quot.sound]
  temporary Statement.olean removed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets agree
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0594
  exit 0: rank 255, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0594/{obligation-registry.json,typed-graphs.json,validation-specs.json}
  exit 0 for each file
rg -n '\b(sorry|admit|axiom|proof_wanted)\b' Stage1_Instances/THM-M-0594/ObligationTree.lean
  exit 1 (expected): no prohibited proof escape or declaration
git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The initial Lean command is retained as evidence of a local-module search-path
mistake, not a dependency blocker. The corrected narrow command first creates
the required local `Statement.olean`, elaborates the conditional composition,
reports its axiom surface, and removes the temporary artifact.

The structural checker verifies frozen denominators, all required node fields,
typed graph separation, reciprocal proof/composition edges, adjacency indexes,
acyclic root reachability, structured recipe coverage, closure boundaries, and
hygiene. Lean checks that the final witness package has exactly the canonical
root type. It does not create that witness: the unrestricted theorem remains
`[H1, M3, R3]`, with no audit-completion or theorem-completion claim.
