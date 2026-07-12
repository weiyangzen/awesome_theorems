# THM-M-0317 obligation-tree validation

Item: `S56-M-0317-OBLIGATION_TREE`. Base revision:
`28be4ce7383f582503e6b54f645e2ca0e955d9de`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-0317/build_obligation_artifacts.py
  exit 0
  aa74ec72cb476dc8775c8c3f33afbe71b8ea6e6d1cd3422c1e19625e18a8d68d

python3 Stage1_Instances/THM-M-0317/check_obligation_tree.py
  exit 0
  PASS THM-M-0317 obligation tree: 17 obligations, 33 typed edges
  registry denominator sha256: aa74ec72cb476dc8775c8c3f33afbe71b8ea6e6d1cd3422c1e19625e18a8d68d
  root closure: open (M3); approximation and compactness-limit packages remain M4

cd Stage1_Instances/THM-M-0317 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0317 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_approximation_and_limit depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0317
  exit 0: rank 683, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0317
  exit 0; no output
```

The first Lean invocation is retained as exact evidence: Lake resolved the pinned dependency
environment, but this clone has no Elan default. The successful retry names the already-installed
pinned Lean 4.29.0 binary and uses Lake only to derive the same `LEAN_PATH`.

The checks validate source and anchor freeze hashes, the denominator, full required node schema,
typed graph separation, reciprocal proof/composition edges, adjacency, acyclicity and root
reachability, validation-recipe coverage, placeholder hygiene, exact-root conditional composition,
and its axiom surface. They do not prove either explicit package premise. No accepted receipt,
audit completion, or theorem completion is claimed; master acceptance remains required.
