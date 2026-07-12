# THM-M-1006 obligation-tree validation

Item: `S56-M-1006-OBLIGATION_TREE`. Base revision:
`688f1e598934169a383f99a0cde9d998eca49972`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1006/build_obligation_artifacts.py
  exit 0
  wrote 18 obligations and 49 typed edges
  12818dc1f1f77555b23c3fea780e482518d1d5c196dc1390c8175d00914dac6f

python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py
  exit 0
  PASS THM-M-1006 obligation tree: 18 obligations, 49 typed edges
  registry denominator sha256: 12818dc1f1f77555b23c3fea780e482518d1d5c196dc1390c8175d00914dac6f
  root closure: open (M3); lower and upper directional BDG packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1006/Statement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-1006/ObligationTree.lean
  exit 1
  Statement.lean elaborated, then the second command reported unknown module prefix `Statement`.

cd Stage1_Instances/THM-M-1006 &&
  LEAN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
    "$LEAN" ObligationTree.lean
  exit 0
  root_of_directional_BDG depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 -m json.tool Stage1_Instances/THM-M-1006/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file
python3 Docs/tools/check_stage1_standard.py
  exit 0: 1546 uniform-L0 targets and all standard structure passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546
python3 scripts/stage1_target.py show THM-M-1006
  exit 0: rank 286, planned, L0/rework-required, theorem_complete false
rg -n -w 'sorry|admit|axiom|sorryAx' Stage1_Instances/THM-M-1006 --glob '*.lean'
  exit 1: expected no-match result; no forbidden Lean proof token found
git diff --check -- Stage1_Instances/THM-M-1006
  exit 0; no output
```

The first Lean attempt is retained as exact evidence rather than hidden. It elaborated the statement
but could not resolve a sibling file as a module because no local `Statement.olean` existed in the
search path. The successful narrow retry used `lake env which lean` and Lake's pinned `LEAN_PATH`,
created only a temporary owned-path `Statement.olean`, and removed it afterward.

These checks validate source and anchor fingerprints, the frozen denominator, eligibility lists,
node ledgers, typed reciprocal proof edges, graph adjacency and reachability, recipe coverage,
placeholder hygiene, elaboration, exact conditional root output, and its axiom surface. They do not
prove `LowerBDG` or `UpperBDG`. There is no accepted receipt; master acceptance remains required.
