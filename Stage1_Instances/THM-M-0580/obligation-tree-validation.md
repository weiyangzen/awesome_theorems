# THM-M-0580 obligation-tree validation

Item: `S56-M-0580-OBLIGATION_TREE`  
Base revision: `ae68d10d70accbf26b8c8c53097b02a2ae2fa561`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

The worker reused the existing pinned Lake environment. It did not update,
fetch, clone, or build dependencies, and no network access was needed.

## Exact commands and outcomes

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546,
  all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0580
  exit 0
  rank 115; planned; L0/rework_required; theorem_complete false

python3 Stage1_Instances/THM-M-0580/build_obligation_artifacts.py
  exit 0
  46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d

python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py
  exit 0
  PASS THM-M-0580 obligation tree: 20 obligations, 42 typed edges
  registry denominator sha256:
  46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d
  root closure: open (M4); smoothing and smooth Perelman packages remain unproved

python3 -m json.tool Stage1_Instances/THM-M-0580/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-0580/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-0580/validation-specs.json
  exits 0; all structured artifacts parse as JSON

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0580/ObligationTree.lean
  exit 1
  expected scoped-import failure: unknown module prefix `Statement` because
  the sibling source had not yet been elaborated to `Statement.olean`

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_LIB=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0580 &&
  LEAN_PATH="$LEAN_LIB" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=".:$LEAN_LIB" "$LEAN_BIN" ObligationTree.lean)
rm -f Stage1_Instances/THM-M-0580/Statement.olean
  exit 0
  root_of_smoothing_and_smooth_poincare elaborated with exact result
  PerelmanPoincareTarget and reported only [propext, Classical.choice,
  Quot.sound]; no sorryAx
```

The first direct Lean command is recorded rather than hidden. The successful
retry still uses the exact pinned `lake env` executable and dependency search
path, creates only a temporary sibling `.olean`, and removes it immediately.

## Validated boundary

The checker binds the registry to the statement and anchor-audit hashes,
recomputes the 20-node denominator, checks every required node field and
prospective step budget, checks typed graph adjacency and reciprocal proof
edges, rejects proof cycles, verifies root reachability and structured recipe
coverage, and scans the Lean composition module for forbidden declarations.

This validates the obligation-tree phase only. The conditional composition has
two open inputs: compatible smoothing and the smooth Perelman package. It does
not establish H0, R0, root machine closure, audit completion, theorem
completion, release evidence, or master acceptance.
