# THM-M-0590 obligation-tree validation

Item: `S56-M-0590-OBLIGATION_TREE`. Base revision:
`c299e0512fb2c1371ed98a055c95169a2c981ff6`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused. No update, build, dependency clone, or fetch was run.

```text
python3 Stage1_Instances/THM-M-0590/build_obligation_artifacts.py
  exit 0
  2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8

python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py
  exit 0
  PASS THM-M-0590 obligation tree: 17 obligations, 37 typed edges
  registry denominator sha256: 2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8
  root closure: open (M4); forward and backward BDF packages remain M4

cd Stage1_Instances/THM-M-0590 &&
  LEAN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" ObligationTree.lean
  exit 0
  THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop
  'THMM0590.root_of_directional_packages' depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0590
  exit 0: rank 630, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0590
  exit 0; no output
```

An initial direct invocation from `Formalizations/Lean` failed with exit 1
because `import Statement` requires a local compiled `Statement.olean`. A retry
using `lake env lean` from the target directory also failed with exit 1 because
this worker has no Elan default toolchain. The successful command above uses the
exact Lean executable returned by the pinned `lake env which lean` and the same
Lake-derived `LEAN_PATH`; these failed attempts are recorded rather than hidden.

The checks validate the frozen denominator, required node fields, typed graph
adjacency and reciprocal proof edges, proof-DAG reachability, structured recipe
coverage, placeholder hygiene, exact conditional root output, and its current
axiom surface. They do not prove either directional package. No theorem receipt
or completion is claimed; master acceptance of this obligation-tree item is
still required.
