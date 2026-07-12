# THM-M-0324 obligation-tree validation

Item: `S56-M-0324-OBLIGATION_TREE`. Base revision:
`106084d7f6343f3046dfb9e108503edbcdc86191`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused read-only; no update, build, fetch, clone, or dependency
mutation was run.

```text
python3 Stage1_Instances/THM-M-0324/build_obligation_artifacts.py
  exit 0
  8bfbe3412a12fb869340a975b51d7b8d48ecf9ad1a529f9c9698c99941ff101b

python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py
  exit 0
  PASS THM-M-0324 obligation tree: 15 obligations, 55 typed edges
  registry denominator sha256: 8bfbe3412a12fb869340a975b51d7b8d48ecf9ad1a529f9c9698c99941ff101b
  root closure: open (M3); Enflo construction, exact approximation interface,
  source map, and foundation audit remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0324
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  noBasis_of_basis_implies_property depends on axioms:
    [propext, Classical.choice, Quot.sound]
  root_of_witness depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

The first direct command from `Formalizations/Lean`,
`lake env lean ../../Stage1_Instances/THM-M-0324/ObligationTree.lean`, exited 1
because the sibling `Statement` module had no olean in Lake's search path. The
corrected command above uses the exact Lake-selected Lean executable and
`LEAN_PATH`, creates a temporary `Statement.olean` only inside the owned path,
checks the composition module, and removes the temporary file.

The structural checker binds the registry to the statement and anchor-audit
hashes; recomputes all eligibility denominators; checks the complete node
schema and semantic ledgers; checks graph adjacency, reciprocal proof edges,
root reachability, acyclicity, structured recipe coverage, open-cut honesty,
and placeholder hygiene. Lean checks the exact terminal logical compositions.
Neither check proves an Enflo space, an approximation-property theorem, any
open analytic child, source acceptance, or theorem completion. Master
acceptance remains required.
