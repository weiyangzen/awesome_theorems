# THM-M-0994 obligation-tree validation

Item: `S56-M-0994-OBLIGATION_TREE`. Base revision:
`43150dedcc9b6a67cc01da20233a7ab0c4c351c0`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, or dependency mutation ran.

```text
python3 Stage1_Instances/THM-M-0994/build_obligation_artifacts.py
  exit 0
  wrote 13 obligations, 26 typed edges
  registry denominator sha256: e3e305b55e5a0bd1fd34779f06f57633dc6aef37265b885c8ccd02e005201278

python3 Stage1_Instances/THM-M-0994/check_obligation_tree.py
  exit 0
  PASS THM-M-0994 obligation tree: 13 obligations, 26 typed edges
  registry denominator sha256: e3e305b55e5a0bd1fd34779f06f57633dc6aef37265b885c8ccd02e005201278
  root remains open at M1; cut set: T-PROXY, L-PROXY-ALG, B-ZERO-WIDTH

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0994/ObligationTree.lean
  exit 0
  both pinned mathlib declarations typechecked
  root_compose depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets
python3 scripts/stage1_target.py show THM-M-0994
  exit 0: rank 274, planned, theorem_complete false
python3 -m json.tool <each of obligation-registry.json,
  typed-graphs.json, validation-specs.json>
  exit 0 for all three files
git diff --check -- Stage1_Instances/THM-M-0994
  exit 0; no output
```

The structural validator checks source-binding hashes, the frozen denominator,
eligibility projections, required node ledgers, all seven typed graph kinds,
adjacency indexes, reciprocal proof edges, acyclicity and root reachability,
validation-recipe coverage, placeholder hygiene, and the explicit open-root
boundary. Lean checks the conditional child-to-parent composition and reports
no unexpected axioms. This is node-specific self-test evidence, not an accepted
receipt or a proof of either interface premise. Master acceptance remains
required; audit and theorem completion remain false.
