# THM-M-0312 obligation-tree validation

Item: `S56-M-0312-OBLIGATION_TREE`. Base revision:
`106084d7f6343f3046dfb9e108503edbcdc86191`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
dependency update, build, fetch, or clone ran.

```text
python3 Stage1_Instances/THM-M-0312/build_obligation_artifacts.py
  exit 0
  78cf97375434e73af94eb3ae876c9f0fe84e5721e96da67cec19340e890548ff

python3 Stage1_Instances/THM-M-0312/check_obligation_tree.py
  exit 0
  PASS THM-M-0312 obligation tree: 15 obligations, 28 typed edges
  registry denominator sha256: 78cf97375434e73af94eb3ae876c9f0fe84e5721e96da67cec19340e890548ff
  root closure: open; exact M0-W candidate awaits proof, provenance, trust, and acceptance gates

cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0312/ObligationTree.lean
  exit 1
  unknown module prefix 'Statement'

cd Stage1_Instances/THM-M-0312 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0312 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_equicontinuity_packages depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0312
  exit 0: rank 814, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0312 .stage1-worker-selftest.json
  exit 0; no output
```

The first Lean attempt lacked the local module search path. The second established that this clone
has no Elan default even though Lake can expose the pinned dependency path. The successful narrow
retry used the already-installed pinned Lean 4.29.0 executable and Lake-derived `LEAN_PATH`.

The checks cover frozen hashes and denominators, complete node fields, reciprocal typed proof
edges, graph adjacency, acyclicity and root reachability, unique terminal-body accounting, recipe
coverage, placeholder hygiene, and the exact checked composition output. The exact mathlib proof is
still only a candidate: proof acceptance, full provenance/trust closure, source review, R0, hermetic
validation, and release remain later phases. No accepted receipt or theorem completion is claimed.
