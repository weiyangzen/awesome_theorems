# THM-M-1527 obligation-tree validation

Item: `S56-M-1527-OBLIGATION_TREE`. Base revision:
`6afdcb2c5487434cce7acf7aeb8ed471faf92666`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1527/build_obligation_artifacts.py
  exit 0
  198872182d30c9176fb209b30c22643ab48a26204257acca1f8f85ab72503856

python3 Stage1_Instances/THM-M-1527/check_obligation_tree.py
  exit 0
  PASS THM-M-1527 obligation tree: 10 obligations, 21 typed edges
  registry denominator sha256: 198872182d30c9176fb209b30c22643ab48a26204257acca1f8f85ab72503856
  root closure: open (M3); only conditional propositional assembly is checked

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

cd Stage1_Instances/THM-M-1527 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-1527 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  assemble_from_component_equivalences depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.
```

The failed direct `lake env lean` invocation is retained: Lake exposes the pinned dependency
environment, but this clone has no Elan default. The successful retry uses the already-installed
pinned Lean 4.29.0 executable and the same Lake-derived `LEAN_PATH`.

These checks validate input hashes, denominator stability, node ledgers, typed reciprocal proof
edges, adjacency, proof-DAG reachability, validation-recipe coverage, placeholder hygiene,
elaboration, and the conditional composition's axiom surface. They do not prove the canonical
root, accept primary-source coverage, or close trust/release gates. Master acceptance remains
required.
