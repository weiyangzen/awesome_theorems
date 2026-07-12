# THM-M-1251 obligation-tree validation

Item: `S56-M-1251-OBLIGATION_TREE`. Base revision:
`98e63368ae23fcc5338261550116996c11891fc1`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1251/build_obligation_artifacts.py
  exit 0
  20de21694a9950367192a122c1ba85de73d93dd5e57a00b08e38394eb705b3dd

python3 Stage1_Instances/THM-M-1251/check_obligation_tree.py
  exit 0
  PASS THM-M-1251 obligation tree: 11 obligations, 32 typed edges
  registry denominator sha256: 20de21694a9950367192a122c1ba85de73d93dd5e57a00b08e38394eb705b3dd
  root release closure: open; exact M0-W anchor is frozen without proof-phase credit

cd Formalizations/Lean &&
  lake env lean ../../../Stage1_Instances/THM-M-1251/ObligationTree.lean
  exit 1
  no such file or directory (error code: 4294967294)
  file: ../../../Stage1_Instances/THM-M-1251/ObligationTree.lean

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1251/ObligationTree.lean
  exit 0
  root_of_importedDefinitionExpansion depends on axioms:
    [propext, Classical.choice, Quot.sound]

cd Formalizations/Lean &&
  python3 Stage1_Instances/THM-M-1251/build_obligation_artifacts.py
  exit 2
  python3: can't open file '.../Formalizations/Lean/Stage1_Instances/THM-M-1251/build_obligation_artifacts.py'

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1251
  exit 0: rank 171, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-1251
  exit 0; no output
```

The first Lean command used one too many parent traversals, and one combined
validation attempt started in the wrong working directory; both failures are
retained as evidence. The corrected commands use the repository root for
Python checks and the pinned Lake environment for Lean, elaborating the
conditional composition with no placeholders.

These checks validate frozen hashes and denominators, mandatory node fields,
all seven typed graph families, reciprocal proof edges, proof-DAG acyclicity
and reachability, structured recipe coverage, hygiene, and exact conditional
child-to-root composition. They do not establish H0, R0, release provenance,
hermetic replay, independent acceptance, or theorem completion. No master
receipt has been issued.
