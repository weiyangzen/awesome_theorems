# THM-M-1014 obligation-tree validation

Item: `S56-M-1014-OBLIGATION_TREE`  
Base revision: `e0e1658c48365b041b302468a8238be1e1f30f20`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

The existing pinned Lake environment was reused. No dependency update, build, clone, fetch, or
network access was performed. The temporary sibling `Statement.olean` used for the narrow import
check was removed immediately afterward.

## Exact commands and outcomes

```text
python3 Stage1_Instances/THM-M-1014/build_obligation_artifacts.py
  exit 0
  denominator 2547bce4e55d4d787d3e3224fc97ca57424e6916f36a3a09e0101560ba58e07b

python3 Stage1_Instances/THM-M-1014/check_obligation_tree.py
  exit 0
  PASS THM-M-1014 obligation tree: 14 obligations, 22 typed edges
  root closure: open (M1); pinned exact bridge acceptance remains assigned to proof node

python3 -m json.tool Stage1_Instances/THM-M-1014/obligation-registry.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1014/typed-graphs.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1014/validation-specs.json >/dev/null
  exits 0; all structured artifacts parse

cd Stage1_Instances/THM-M-1014
LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean)
LEAN_PATH_BASE=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" ObligationTree.lean
status=$?
rm -f Statement.olean
exit $status
  exit 0
  the frozen StatementShape and the exact conditional composition elaborated
  #print axioms root_of_continuousMappingTerminal: [propext, Classical.choice, Quot.sound]
  no sorryAx reported

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1014
  exit 0; rank 293, planned, legacy artifacts unaccepted, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-1014 .stage1-worker-selftest.json
  exit 0; no scoped whitespace errors
```

## Validated boundary

The checker binds the registry to the exact statement and anchor-audit hashes, recomputes the
14-obligation denominator, requires all node fields and bounded ledgers, verifies unique terminal
body accounting, typed adjacency, reciprocal proof/composition edges, acyclicity, required-machine
reachability, and validation-recipe coverage, and scans the Lean composition module for forbidden
proof escapes.

This self-tests the obligation-tree deliverable only. `M1014-X-PINNED` remains the explicit root cut
because accepting the pinned terminal proof body is assigned to `S56-M-1014-PROOF`. Human-source
`H0`, readable `R0`, proof acceptance, hermetic validation, audit completion, theorem completion,
release, and master acceptance remain open.
