# THM-M-1247 obligation-tree validation

Item: `S56-M-1247-OBLIGATION_TREE`. Base revision:
`50fa1bbf0f067f9f3ad127ab97d86d255c928a2b`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, or dependency mutation ran.

```text
python3 Stage1_Instances/THM-M-1247/build_obligation_artifacts.py
  exit 0
  9df3b5e945d93397440974dd4952e5216934cff0f3e4d83efbd9f1bcdc79a590

python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py
  exit 0
  PASS THM-M-1247 obligation tree: 13 obligations, 34 typed edges
  registry denominator sha256: 9df3b5e9...79a590
  root closure: open (M3); six analytic obligations remain M4

cd Stage1_Instances/THM-M-1247 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-1247 &&
  LEAN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" ObligationTree.lean
  exit 0
  root_of_coreRellichEstimate depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check

python3 Stage1_Instances/THM-M-1247/check_statement.py
  exit 0; all four structural mutations distinguished; expression SHA-256
  4697dbba...5c90e
python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py
  exit 0; three mathlib candidate families checked; terminal result open
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1247
  exit 0; rank 427, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1247 .stage1-worker-selftest.json
  exit 0; no output
```

The initial direct `lake env lean` failure is retained as evidence: this clone
has no Elan default. The successful retry uses the already installed exact
pinned Lean 4.29.0 executable with Lake's pinned `LEAN_PATH`.

These checks validate the frozen denominator, required node fields, typed and
reciprocal proof edges, adjacency, acyclic root reachability, recipe coverage,
Lean elaboration, exact conditional root transport, and axiom surface. They do
not prove the explicit `CoreRellichEstimate` premise. No theorem-completion or
accepted-receipt claim is made; master acceptance is still required.
