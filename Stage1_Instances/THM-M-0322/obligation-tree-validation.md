# THM-M-0322 obligation-tree validation

Item: `S56-M-0322-OBLIGATION_TREE`. Base revision:
`106084d7f6343f3046dfb9e108503edbcdc86191`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake artifacts and ran no update, build, clone, or fetch.

```text
python3 Stage1_Instances/THM-M-0322/build_obligation_artifacts.py
  exit 0
  d98f83a7242eccacc32e330ba44ed8c7a259e6f6df76e4959c89d26628d981a3

python3 Stage1_Instances/THM-M-0322/check_obligation_tree.py
  exit 0
  PASS THM-M-0322 obligation tree: 19 obligations, 38 typed edges
  registry denominator sha256: d98f83a7242eccacc32e330ba44ed8c7a259e6f6df76e4959c89d26628d981a3
  root closure: open (M3); reverse inclusion and source/trust/provenance gates remain open

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0322/Statement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-0322/ObligationTree.lean
  exit 1 on the second command
  unknown module prefix 'Statement' because a standalone source invocation does
  not create Statement.olean in the target directory

LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)
cd Stage1_Instances/THM-M-0322
LEAN_PATH="$LEAN_PATH" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  hullExtreme_subset axioms: [propext, Classical.choice, Quot.sound]
  root_of_inclusions axioms: [propext, Classical.choice, Quot.sound]
  only unused-context linter warnings for hscomp and hconv in the pure
  antisymmetry composition; Statement.olean removed after the scoped check

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0322
  exit 0: rank 819, planned, theorem_complete false
```

The structural validator checks source-binding hashes, the frozen denominator,
all required node fields and ledgers, graph adjacency, reciprocal proof edges,
proof-DAG acyclicity and exact reachability, validation-spec coverage, and the
open closure boundary. Lean checks the easy inclusion and exact composition
without placeholders. The initial import-path failure is retained as evidence;
the successful narrow retry uses the same pinned Lake-derived environment.

This is nonrelease worker evidence. The reverse-inclusion package, complete
transitive provenance/trust, human-source and readable review, master receipt,
and theorem completion remain open.
