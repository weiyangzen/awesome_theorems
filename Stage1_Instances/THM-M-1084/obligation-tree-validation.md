# THM-M-1084 obligation-tree validation

Item: `S56-M-1084-OBLIGATION_TREE`  
Date: `2026-07-12`  
Base revision: `67664ce109cd6d2cb390a1bab66d3f84f38a8e35`

Validation ran in the worker clone using only the existing pinned Lake artifacts. No dependency
update, build, clone, or fetch was run.

```text
python3 Stage1_Instances/THM-M-1084/build_obligation_artifacts.py
  exit 0
  a2bf7a0e46b0ca64f3ce1259043f8e1f7c85975bb4762a9e2a5256709555111a

python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py
  exit 0
  PASS THM-M-1084 obligation tree: 16 obligations, 36 typed edges
  registry denominator sha256: a2bf7a0e46b0ca64f3ce1259043f8e1f7c85975bb4762a9e2a5256709555111a
  root closure: open (M3); integrability and exact entropy packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1084/Statement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-1084/ObligationTree.lean
  exit 1
  Statement.lean elaborated; ObligationTree import failed because the target directory is not a
  module root in the Lake LEAN_PATH.

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1084
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_integrability_and_entropy_packages elaborated
  axioms: [propext, Classical.choice, Quot.sound]
  existing Statement.lean unused-variable warning only

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1,546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1,546 unique ordered targets
python3 scripts/stage1_target.py show THM-M-1084
  exit 0: rank 526, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json, validation-specs.json
  exit 0 for all three files
git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json
  exit 0; no output
```

The initially failed import command is retained rather than hidden. The successful narrow retry
uses the exact Lean executable selected by `lake env`, Lake's pinned dependency path, and a temporary
local `Statement.olean`, which was removed immediately after checking.

This self-tests the immutable denominator hash, registry eligibility projections, graph adjacency,
reciprocal proof composition, DAG acyclicity, semantic ledgers, recipe coverage, exact conditional
root composition, and its axiom surface. It does not prove either package premise. The root remains
`M3`; audit completion and theorem completion remain false; master acceptance is still required.
