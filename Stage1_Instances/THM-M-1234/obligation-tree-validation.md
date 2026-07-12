# THM-M-1234 obligation-tree validation

Item: `S56-M-1234-OBLIGATION_TREE`. Base revision:
`8d91c34cbb9c630032c5b7d6dbbd0d1df599f4fa`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned
Lake environment. No update, dependency fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1234/build_obligation_artifacts.py
  exit 0
  cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d

python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py
  exit 0
  PASS THM-M-1234 obligation tree: 14 obligations, 28 typed edges
  registry denominator sha256: cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d
  root closure: open (M3); construction and equation/trace packages remain M4

cd Formalizations/Lean && lake env lean -o \
  ../../Stage1_Instances/THM-M-1234/Statement.olean \
  ../../Stage1_Instances/THM-M-1234/Statement.lean
  exit 1
  input file must be contained in the Formalizations/Lean root directory

LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-1234
LEAN_PATH="$LEAN_PATH" "$LEAN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  Statement : Prop elaborated
  root_of_construction_and_closure depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

The failed first invocation is retained as exact evidence: Lean refuses to
emit an olean outside the selected package root. The successful retry still
uses `lake env` to select the pinned Lean executable and dependency path, then
performs the narrow two-module elaboration from the owned directory.

The structural check validates source hashes, frozen denominators, node
ledgers and budgets, all seven graph types, reciprocal proof edges, adjacency,
proof-DAG acyclicity and reachability, validation recipe coverage, and the
open closure boundary. Elaboration validates the conditional construction into
the exact root and reports its axiom surface. It does not prove either package
premise. Master acceptance and every later phase remain open.
