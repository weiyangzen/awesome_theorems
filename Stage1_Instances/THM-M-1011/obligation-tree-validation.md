# THM-M-1011 obligation-tree validation

Item: `S56-M-1011-OBLIGATION_TREE`  
Base revision: `b464f991efe5978f547092d80ac4bce99d6485c3`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

The existing pinned Lake environment was reused. No dependency update, build,
clone, fetch, or network access was performed, and the temporary sibling
`Statement.olean` was removed after scoped elaboration.

## Exact commands and outcomes

```text
python3 Stage1_Instances/THM-M-1011/build_obligation_artifacts.py
  exit 0
  denominator 3dd41addcf34fd9ca7d89e9d2231337be0e01df77f497acdcefff743020bdd90

python3 Stage1_Instances/THM-M-1011/check_obligation_tree.py
  exit 0
  PASS THM-M-1011 obligation tree: 14 obligations, 35 typed edges
  root closure: open (M5); exact frozen context does not supply T2Space X

cd Stage1_Instances/THM-M-1011
LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean)
LEAN_PATH_BASE=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  compact_to_tight, tight_to_compact_of_t2, and canonical_of_t2 elaborated
  #print axioms canonical_of_t2: [propext, Classical.choice, Quot.sound]
  no sorryAx reported

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1011
  exit 0; rank 260, planned, L0/rework_required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-1011/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1011/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1011/validation-specs.json
python3 -m json.tool Stage1_Instances/THM-M-1011/instance.json
  exits 0; all four structured artifacts parse

git diff --check -- Stage1_Instances/THM-M-1011 .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

## Validated boundary

The checker binds the registry to the exact statement and anchor-audit hashes,
recomputes the 14-node denominator, requires every node field and budget,
checks typed adjacency and reciprocal proof/composition edges, rejects cycles,
checks root reachability and structured recipe coverage, and scans the Lean
module for forbidden declarations.

This self-tests the obligation-tree deliverable only. The exact root is not
proved: `M1011-N-SEPARATION` remains the immediate cut set. H0, R0, audit
completion, theorem completion, hermetic release, and master acceptance remain
open.
