# THM-M-1235 obligation-tree validation

Item: `S56-M-1235-OBLIGATION_TREE`  
Base revision: `9258763ef5d98df2b13458756f43399dd7e63278`

Validation ran in the worker clone on 2026-07-12. It reused the existing
pinned Lean and Lake dependency environment. No dependency update, fetch,
clone, or build was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
  300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1235
  exit 0
  rank 159; planned; L0/rework_required; theorem_complete false

python3 Stage1_Instances/THM-M-1235/build_obligation_artifacts.py
  exit 0
  9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba

python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py
  exit 0
  PASS THM-M-1235 obligation tree: 15 obligations, 37 typed edges
  registry denominator sha256:
    9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba
  root closure: open (M3); existence and uniqueness packages remain M4

LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
BASE_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1235
LEAN_PATH="$BASE_PATH" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$BASE_PATH" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_existence_and_uniqueness depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 -m json.tool Stage1_Instances/THM-M-1235/obligation-registry.json
python3 -m json.tool Stage1_Instances/THM-M-1235/typed-graphs.json
python3 -m json.tool Stage1_Instances/THM-M-1235/validation-specs.json
  each exit 0

git diff --check -- Stage1_Instances/THM-M-1235
  exit 0; no output
```

The structural check recomputes the statement and predecessor-audit hashes,
the canonical denominator, all required node fields, typed edge adjacency,
reciprocal `proof_requires`/`composes` pairs, proof-DAG acyclicity and root
reachability, recipe coverage, closure boundary, and placeholder hygiene. The
Lean check elaborates the frozen statement and the exact conditional root
composition using the pinned 4.29.0 executable and Lake-derived dependency
path. The temporary `Statement.olean` was removed after validation.

This phase freezes architecture and proves only conditional composition. The
existence and uniqueness packages, native expansion of conditions `(I)`-`(VIII)`,
node-specific H0/R0 review, terminal-body provenance, full validation, and
master acceptance remain open. No theorem-completion claim or accepted receipt
is made.
