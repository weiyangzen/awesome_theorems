# THM-M-0669 obligation-tree validation

Item: `S56-M-0669-OBLIGATION_TREE`. Base revision:
`d4da54fa4b81642d3c351d58820f005903bbe09e`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0669/build_obligation_artifacts.py
  exit 0
  9ec85645aa13399fb7dd6255e1cb66f90fc3694c536f6a282a6b30f19173afb4

python3 Stage1_Instances/THM-M-0669/check_obligation_tree.py
  exit 0
  PASS THM-M-0669 obligation tree: 14 obligations, 49 typed edges
  registry denominator sha256: 9ec85645aa13399fb7dd6255e1cb66f90fc3694c536f6a282a6b30f19173afb4
  root closure: open (M3); one-variable algebraic elimination and formula recursion remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0669
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  Stage1.THM_M_0669.TarskiQuantifierEliminationTarget : Prop
  root_of_elimination depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0669
  exit 0; rank 713, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0669 .stage1-worker-selftest.json
  exit 0
```

The structural checker validates freeze hashes, immutable denominators and
eligibility projections, typed adjacency, reciprocal proof edges, proof-DAG
acyclicity, validation-recipe coverage, and placeholder hygiene. Lean validates
the unchanged exact statement and identity root boundary. The reported axioms
come through the statement's semantic and complete-theory definitions and are
recorded rather than interpreted as proof closure.

This phase does not validate polynomial sign elimination, projection,
formula-recursion composition, source closure, theorem proof, or theorem
completion. The pre-existing untracked canonical `.lake` symlink was reused and
not modified. Master acceptance remains required.
