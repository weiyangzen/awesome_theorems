# THM-M-0161 obligation-tree validation

Item: `S56-M-0161-OBLIGATION_TREE`. Base revision:
`b077d12b80578ad8e0f6d19a4ab2dadabdfe40c8`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused. No
dependency update, fetch, clone, or build was run. The pre-existing untracked
`Formalizations/Lean/.lake` path makes this worker evidence nonrelease evidence.

```text
python3 Stage1_Instances/THM-M-0161/build_obligation_artifacts.py
  exit 0
  48173f90a121c627719e3cadc9a5fd2255e2f805e606b8bfe0f4ae7c5a2dadbe

python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py
  exit 0
  PASS THM-M-0161 obligation tree: 21 obligations, 44 typed edges
  registry denominator sha256: 48173f90...dadbe
  root closure: open (M3); exact existence and uniqueness packages remain M4

cd Stage1_Instances/THM-M-0161 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH="$LEAN_PATH" "$LEAN" -o Statement.olean Statement.lean &&
  LEAN_PATH=".:$LEAN_PATH" "$LEAN" ObligationTree.lean
  exit 0
  root_of_existence_and_uniqueness depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Stage1_Instances/THM-M-0161/check_statement.py
  exit 0
  target expression c140d1d1...f82; four structural mutations distinguished

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0161/AnchorCandidates.lean
  exit 0
  crossProduct and the three pinned ODE declarations elaborate

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0161
  exit 0; rank 660, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0161/{obligation-registry,typed-graphs,validation-specs}.json
  exit 0 for each file
git diff --check -- Stage1_Instances/THM-M-0161
  exit 0; no output
```

An initial direct command, `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-0161/ObligationTree.lean`, exited 1 because the sibling module
`Statement` had not been compiled into the Lean search path. The successful narrow recipe above
uses the exact Lean executable and Lake-derived pinned `LEAN_PATH`, creates only a temporary local
`Statement.olean`, and removes it. A first retry also exposed and corrected parser errors in the new
package signatures; the final recorded recipe passed without `sorryAx`.

The structural check covers immutable input hashes, registry denominator reproduction, unique IDs,
required node fields, step budgets, typed reciprocal proof edges, graph adjacency and acyclicity,
root reachability, structured recipe coverage, and the fail-closed closure boundary. Lean checks the
conditional child-to-parent composition into the exact canonical target. Neither package premise is
proved, so no root proof, source acceptance, audit completion, theorem completion, or accepted
master receipt is claimed.
