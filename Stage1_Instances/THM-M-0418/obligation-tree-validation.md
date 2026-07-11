# THM-M-0418 obligation-tree validation

Item: `S56-M-0418-OBLIGATION_TREE`. Base revision:
`a03622f1a1743344089f13a3a09ec4635f791960`.

Validation ran from the isolated worker clone on 2026-07-12. It reused the
existing pinned Lake dependency artifacts; no update, fetch, clone, dependency
build, or network access was performed.

```text
python3 Stage1_Instances/THM-M-0418/build_obligation_artifacts.py
  exit 0
  ffe074d5c0109ded031f6edfafde1b8498531bd63f4a41a27ba2f4fb1ceb79de

python3 Stage1_Instances/THM-M-0418/check_obligation_tree.py
  exit 0
  PASS THM-M-0418 obligation tree: 14 obligations, 28 typed edges
  registry denominator sha256: ffe074d5c0109ded031f6edfafde1b8498531bd63f4a41a27ba2f4fb1ceb79de
  root machine closure: M0-W via one pinned mathlib terminal body; theorem completion remains false

cd Stage1_Instances/THM-M-0418 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-0418 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  NumberField.exists_ideal_in_class_of_norm_le depends on axioms:
    [propext, Classical.choice, Quot.sound]
  minkowskiIdealClassBound_obligationRoot depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0418
  exit 0: rank 73, planned, theorem_complete false
```

The failed `lake env lean` attempt is retained as evidence: Lake can derive the
pinned dependency path, but this clone has no Elan default. The successful
retry uses the installed executable for the repository-pinned Lean 4.29.0
toolchain and the same Lake-derived `LEAN_PATH`.

These checks cover content hashes, frozen denominators, every required node
field, typed graph adjacency, reciprocal proof/composition edges, proof-DAG
reachability and acyclicity, structured recipe coverage, placeholder hygiene,
kernel elaboration, exact root composition, and the reported axiom surface.
They do not close primary-source, R0, hermetic-release, independent-runner, or
master-acceptance gates. There is no accepted receipt and theorem completion
remains false.
